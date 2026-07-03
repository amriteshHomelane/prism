"""Google Calendar sync. Safe to import even when unconfigured.

Configure by adding [gcp_service_account] and [app] to .streamlit/secrets.toml
(see secrets.toml.example). Until then, is_configured() returns False and the
app falls back to .ics export so you can still validate the workflow.
"""

import streamlit as st

SCOPES = ["https://www.googleapis.com/auth/calendar"]
TZ = "Asia/Kolkata"

TYPE_TAG = {"module": "", "fireside": "[Fireside] ", "assessment": "[Assessment] ", "activity": "[Activity] "}


def is_configured():
    try:
        return "gcp_service_account" in st.secrets and "app" in st.secrets \
            and st.secrets["app"].get("calendar_id")
    except Exception:
        return False


def _service():
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    info = dict(st.secrets["gcp_service_account"])
    kwargs = {"scopes": SCOPES}
    impersonate = st.secrets["app"].get("impersonate")
    if impersonate:
        kwargs["subject"] = impersonate  # domain-wide delegation -> invites send as this user
    creds = service_account.Credentials.from_service_account_info(info, **kwargs)
    return build("calendar", "v3", credentials=creds, cache_discovery=False)


def _body(session, invitee_emails):
    tag = TYPE_TAG.get(session.get("type", "module"), "")
    return {
        "summary": f'{tag}{session["title"]} — {session["pod"]}',
        "location": session.get("loc", ""),
        "description": (f'Faculty: {session.get("faculty","")} | Mode: {session.get("mode","")} '
                        f'| Status: {session.get("status","")}\n{session.get("note","")}'),
        "start": {"dateTime": f'{session["date"]}T{session["start"]}:00', "timeZone": TZ},
        "end":   {"dateTime": f'{session["date"]}T{session["end"]}:00',   "timeZone": TZ},
        "attendees": [{"email": e} for e in invitee_emails],
        "status": "confirmed" if session.get("status") == "confirmed" else "tentative",
    }


def upsert_event(session, invitee_emails):
    """Create or update the calendar event; returns the Google event id."""
    svc = _service()
    cal = st.secrets["app"]["calendar_id"]
    body = _body(session, invitee_emails)
    if session.get("gcal_id"):
        ev = svc.events().update(calendarId=cal, eventId=session["gcal_id"],
                                 body=body, sendUpdates="all").execute()
    else:
        ev = svc.events().insert(calendarId=cal, body=body, sendUpdates="all").execute()
    return ev["id"]


# ---- Offline fallback: .ics export (works with zero setup) ----
def _ics_dt(date, time):
    return date.replace("-", "") + "T" + time.replace(":", "") + "00"


def _esc(s):
    return (s or "").replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", " ")


def build_ics(sessions, invitees_fn):
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Prism Academy//Calendar//EN", "CALSCALE:GREGORIAN"]
    for s in sessions:
        tag = TYPE_TAG.get(s.get("type", "module"), "")
        lines += ["BEGIN:VEVENT", f'UID:prism-{s.get("id","")}@prismacademy',
                  f'DTSTART:{_ics_dt(s["date"], s["start"])}', f'DTEND:{_ics_dt(s["date"], s["end"])}',
                  f'SUMMARY:{_esc(tag + s["title"] + " — " + s["pod"])}']
        if s.get("loc"):
            lines.append(f'LOCATION:{_esc(s["loc"])}')
        lines.append(f'DESCRIPTION:{_esc("Faculty: " + s.get("faculty","") + " | Mode: " + s.get("mode",""))}')
        for e in invitees_fn(s["pod"]):
            lines.append(f'ATTENDEE;ROLE=REQ-PARTICIPANT;RSVP=TRUE;CN={e}:mailto:{e}')
        lines += [f'STATUS:{"CONFIRMED" if s.get("status")=="confirmed" else "TENTATIVE"}', "END:VEVENT"]
    lines.append("END:VCALENDAR")
    return "\r\n".join(lines)

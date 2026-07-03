"""Google Calendar sync. Off until GOOGLE_SA_JSON + GOOGLE_CALENDAR_ID are set."""

from django.conf import settings

SCOPES = ["https://www.googleapis.com/auth/calendar"]
TZ = "Asia/Kolkata"
TYPE_TAG = {"module": "", "fireside": "[Fireside] ", "assessment": "[Assessment] ", "activity": "[Activity] "}


def is_configured():
    return bool(settings.GOOGLE_SA_JSON and settings.GOOGLE_CALENDAR_ID)


def _service():
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    kwargs = {"scopes": SCOPES}
    if settings.GOOGLE_IMPERSONATE:
        kwargs["subject"] = settings.GOOGLE_IMPERSONATE
    creds = service_account.Credentials.from_service_account_file(settings.GOOGLE_SA_JSON, **kwargs)
    return build("calendar", "v3", credentials=creds, cache_discovery=False)


def _body(s, invitees):
    tag = TYPE_TAG.get(s.type, "")
    return {
        "summary": f"{tag}{s.title} — {s.pod.short}",
        "location": s.loc or "",
        "description": f"Faculty: {s.faculty} | Mode: {s.get_mode_display()} | Status: {s.get_status_display()}\n{s.note}",
        "start": {"dateTime": f"{s.date.isoformat()}T{s.start}:00", "timeZone": TZ},
        "end": {"dateTime": f"{s.date.isoformat()}T{(s.end or s.start)}:00", "timeZone": TZ},
        "attendees": [{"email": e} for e in invitees],
        "status": "confirmed" if s.status == "confirmed" else "tentative",
    }


def upsert_event(session, invitees):
    svc = _service()
    cal = settings.GOOGLE_CALENDAR_ID
    body = _body(session, invitees)
    if session.gcal_id:
        ev = svc.events().update(calendarId=cal, eventId=session.gcal_id, body=body, sendUpdates="all").execute()
    else:
        ev = svc.events().insert(calendarId=cal, body=body, sendUpdates="all").execute()
    return ev["id"]


# ---- .ics fallback (works with no Google setup) ----
def _esc(s):
    return (s or "").replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", " ")


def build_ics(sessions):
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Prism Academy//Calendar//EN", "CALSCALE:GREGORIAN"]
    for s in sessions:
        tag = TYPE_TAG.get(s.type, "")
        d = s.date.isoformat().replace("-", "")
        lines += ["BEGIN:VEVENT", f"UID:prism-{s.id}@prismacademy",
                  f"DTSTART:{d}T{s.start.replace(':', '')}00",
                  f"DTEND:{d}T{(s.end or s.start).replace(':', '')}00",
                  f"SUMMARY:{_esc(tag + s.title + ' — ' + s.pod.short)}"]
        if s.loc:
            lines.append(f"LOCATION:{_esc(s.loc)}")
        lines.append(f"DESCRIPTION:{_esc('Faculty: ' + s.faculty + ' | Mode: ' + s.get_mode_display())}")
        for e in s.pod.invitees():
            lines.append(f"ATTENDEE;ROLE=REQ-PARTICIPANT;RSVP=TRUE;CN={e}:mailto:{e}")
        lines += [f"STATUS:{'CONFIRMED' if s.status == 'confirmed' else 'TENTATIVE'}", "END:VEVENT"]
    lines.append("END:VCALENDAR")
    return "\r\n".join(lines)

"""Prism Academy — Session Calendar (Streamlit).

Run locally to validate:  streamlit run app.py
No Google setup needed to check it — data persists to data_store.json and you
can export .ics. Add secrets later to turn on live Google Calendar sync.
"""

import datetime as dt

import streamlit as st
from streamlit_calendar import calendar

import seed_data
import store
import calendar_sync as gc

st.set_page_config(page_title="Prism Academy — Session Calendar", page_icon="📅", layout="wide")

POD_COLORS = {p["short"]: p["color"] for p in seed_data.PODS}
POD_FULL = {p["short"]: p["name"] for p in seed_data.PODS}
POD_NAMES = list(POD_COLORS)
TYPES = ["module", "fireside", "assessment", "activity"]


# ------------------------------------------------------------------ identity
def resolve_role(email):
    email = (email or "").lower()
    if email == seed_data.ADMIN_EMAIL.lower():
        return "admin"
    leads = store.get_pod_leads()
    owners = set()
    for v in leads.values():
        owners.add((v.get("owner") or "").lower())
        owners.add((v.get("lead") or "").lower())
    return "pod" if email in owners else "view"


# In real deployment, replace this block with st.login()/st.user (see README).
with st.sidebar:
    st.markdown("### Prism Academy")
    st.caption("Session calendar")
    mode = st.radio("Preview as", ["Program admin", "Pod owner", "Others"], key="rolepick")
    role = {"Program admin": "admin", "Pod owner": "pod", "Others": "view"}[mode]
    can_edit = role in ("admin", "pod")
    st.caption("Prototype: role is a simulator. Real login maps identity automatically.")
    st.divider()
    pod_filter = st.selectbox("Filter by pod", ["All pods"] + POD_NAMES)
    st.divider()
    st.caption(f"Data source: {store.BACKEND}")

st.title("Prism Academy — Session Calendar")
st.caption("Faculty sessions across pods, month on month. "
           + ("Full access." if role == "admin" else "Edit access." if role == "pod" else "View only."))

sessions = store.get_sessions()
if pod_filter != "All pods":
    sessions = [s for s in sessions if s["pod"] == pod_filter]

tab_cal, tab_sessions, tab_people = st.tabs(["📅 Calendar", "📋 Sessions", "👥 Participants & leads"])

# ------------------------------------------------------------------ calendar
with tab_cal:
    events = [{
        "id": s["id"],
        "title": f'{s["title"]} · {s["faculty"]}',
        "start": f'{s["date"]}T{s["start"]}:00',
        "end": f'{s["date"]}T{s["end"]}:00',
        "backgroundColor": POD_COLORS.get(s["pod"], "#4A6741"),
        "borderColor": POD_COLORS.get(s["pod"], "#4A6741"),
    } for s in sessions]
    calendar(events=events, options={
        "initialView": "dayGridMonth",
        "initialDate": "2026-06-01",
        "headerToolbar": {"left": "prev,next today", "center": "title", "right": "dayGridMonth,listMonth"},
        "height": 720,
    }, key="cal")

    st.markdown("**Programs:** " + "  ".join(
        f'<span style="color:{POD_COLORS[p]}">■</span> {p}' for p in POD_NAMES), unsafe_allow_html=True)

    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        if gc.is_configured():
            if st.button("🔄 Sync visible sessions to Google Calendar", disabled=not can_edit):
                ok = 0
                for s in sessions:
                    try:
                        gid = gc.upsert_event(s, store.invitees(s["pod"]))
                        store.set_gcal_id(s["id"], gid)
                        ok += 1
                    except Exception as e:  # noqa
                        st.warning(f'{s["title"]}: {e}')
                st.success(f"Synced {ok} session(s) to Google Calendar.")
        else:
            st.info("Google Calendar sync not configured yet — using .ics export. See README.")
    with c2:
        ics = gc.build_ics(sessions, store.invitees)
        st.download_button("⬇️ Export .ics (import to Google Calendar)", ics,
                           file_name="prism-sessions.ics", mime="text/calendar")

# ------------------------------------------------------------------ sessions
with tab_sessions:
    if can_edit:
        with st.expander("➕ Add a session", expanded=False):
            with st.form("add_session", clear_on_submit=True):
                a, b = st.columns(2)
                pod = a.selectbox("Pod", POD_NAMES)
                typ = b.selectbox("Type", TYPES)
                title = st.text_input("Title")
                fac = st.text_input("Faculty")
                fk = st.radio("Faculty type", ["internal", "external"],
                              index=0 if seed_data.FACULTY.get(fac, "internal") == "internal" else 1,
                              horizontal=True)
                d = st.date_input("Date", value=dt.date(2026, 6, 1))
                t1, t2 = st.columns(2)
                start = t1.time_input("Start", value=dt.time(11, 0))
                end = t2.time_input("End", value=dt.time(12, 0))
                mode_ = st.radio("Mode", ["virtual", "inperson"], horizontal=True)
                loc = st.text_input("Meeting link / venue")
                status = st.radio("Status", ["proposed", "confirmed"], horizontal=True)
                note = st.text_area("Notes")
                if st.form_submit_button("Save session"):
                    store.save_session({
                        "pod": pod, "type": typ, "title": title, "faculty": fac, "fkind": fk,
                        "date": str(d), "start": start.strftime("%H:%M"), "end": end.strftime("%H:%M"),
                        "mode": mode_, "loc": loc, "status": status, "note": note, "gcal_id": "",
                    })
                    st.success("Saved.")
                    st.rerun()

    st.subheader("Sessions")
    for s in sorted(sessions, key=lambda x: (x["date"], x["start"])):
        badge = "✅" if s["status"] == "confirmed" else "🟡"
        tag = "" if s["type"] == "module" else f' · {s["type"].title()}'
        with st.expander(f'{badge} {s["date"]} {s["start"]}  |  {s["title"]}  ·  {s["pod"]}{tag}'):
            st.write(f'**Faculty:** {s["faculty"]} ({s["fkind"]})   |   **Mode:** {s["mode"]}'
                     f'   |   **Where:** {s.get("loc") or "—"}')
            if s.get("note"):
                st.caption(s["note"])
            inv = store.invitees(s["pod"])
            st.caption(f'Invitees on sync: {len(inv)} — {", ".join(inv[:5])}'
                       + (f' +{len(inv) - 5} more' if len(inv) > 5 else ""))
            if can_edit:
                cc1, cc2 = st.columns([1, 5])
                if cc1.button("Toggle status", key=f'tog{s["id"]}'):
                    s["status"] = "proposed" if s["status"] == "confirmed" else "confirmed"
                    store.save_session(s)
                    st.rerun()
                if cc2.button("Delete", key=f'del{s["id"]}'):
                    store.delete_session(s["id"])
                    st.rerun()

# ------------------------------------------------------------------ people
with tab_people:
    st.subheader("Participants & pod leads")
    if role == "admin":
        st.caption("You can reassign pod owner and content lead, and manage participants.")
    elif role == "pod":
        st.caption("You can manage participants. Pod owner / content lead are set by the program admin.")
    else:
        st.caption("View only.")

    leads = store.get_pod_leads()
    parts = store.get_participants()
    for pod in POD_NAMES:
        with st.expander(f'{pod}  ·  {len(parts.get(pod, []))} participant(s)'):
            st.caption(POD_FULL[pod])
            L = leads.get(pod, {"owner": "", "lead": ""})
            if role == "admin":
                oc, lc = st.columns(2)
                new_o = oc.text_input("Pod owner", L.get("owner", ""), key=f'o{pod}')
                new_l = lc.text_input("Content lead", L.get("lead", ""), key=f'l{pod}')
                if oc.button("Save owner", key=f'so{pod}'):
                    store.set_pod_lead(pod, "owner", new_o.strip().lower()); st.rerun()
                if lc.button("Save lead", key=f'sl{pod}'):
                    store.set_pod_lead(pod, "lead", new_l.strip().lower()); st.rerun()
            else:
                st.write(f'**Pod owner:** {L.get("owner") or "—"}   |   **Content lead:** {L.get("lead") or "—"}')

            st.write("**Participants**")
            for e in parts.get(pod, []):
                org = "DC" if e.lower().endswith("@designcafe.com") else "HL"
                row = st.columns([6, 1])
                row[0].write(f'`{org}`  {e}')
                if can_edit and row[1].button("✕", key=f'rm{pod}{e}'):
                    store.remove_participant(pod, e); st.rerun()
            if can_edit:
                nc = st.columns([6, 1])
                new_e = nc[0].text_input("Add participant email", key=f'add{pod}', label_visibility="collapsed",
                                         placeholder="name@homelane.com or name@designcafe.com")
                if nc[1].button("Add", key=f'addb{pod}') and new_e.strip():
                    store.add_participant(pod, new_e.strip().lower()); st.rerun()

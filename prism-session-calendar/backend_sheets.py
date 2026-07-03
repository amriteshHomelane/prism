"""Google Sheets backend — shared, multi-user, persistent.

Enabled automatically when secrets.toml has [gcp_service_account] and
[sheets].sheet_id (see secrets.toml.example). Share the spreadsheet with the
service-account email as Editor. On first use it creates the Sessions /
Participants / PodLeads tabs and seeds them from seed_data.

Same public API as backend_local, so the app code is identical either way.
All writes use RAW input so dates/times are stored as plain text (no
auto-conversion), and reads are cached briefly and flushed after each write.
"""

import uuid

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

import seed_data

__all__ = ["get_sessions", "save_session", "delete_session", "set_gcal_id",
           "get_participants", "add_participant", "remove_participant",
           "get_pod_leads", "set_pod_lead", "invitees"]

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SESSION_COLS = ["id", "pod", "type", "title", "faculty", "fkind", "date",
                "start", "end", "status", "mode", "loc", "note", "gcal_id"]
RAW = "RAW"


@st.cache_resource
def _spreadsheet():
    creds = Credentials.from_service_account_info(dict(st.secrets["gcp_service_account"]), scopes=SCOPES)
    sh = gspread.authorize(creds).open_by_key(st.secrets["sheets"]["sheet_id"])
    _ensure_seeded(sh)
    return sh


def _ensure_seeded(sh):
    titles = [ws.title for ws in sh.worksheets()]
    if "Sessions" not in titles:
        ws = sh.add_worksheet("Sessions", rows=400, cols=len(SESSION_COLS))
        ws.append_row(SESSION_COLS, value_input_option=RAW)
        rows = []
        for s in seed_data.SESSIONS:
            r = dict(s)
            r.setdefault("id", uuid.uuid4().hex[:10])
            rows.append([str(r.get(c, "")) for c in SESSION_COLS])
        if rows:
            ws.append_rows(rows, value_input_option=RAW)
    if "Participants" not in titles:
        ws = sh.add_worksheet("Participants", rows=800, cols=2)
        ws.append_row(["pod", "email"], value_input_option=RAW)
        rows = [[pod, e] for pod, lst in seed_data.PARTICIPANTS.items() for e in lst]
        if rows:
            ws.append_rows(rows, value_input_option=RAW)
    if "PodLeads" not in titles:
        ws = sh.add_worksheet("PodLeads", rows=50, cols=3)
        ws.append_row(["pod", "owner", "lead"], value_input_option=RAW)
        rows = [[pod, v.get("owner", ""), v.get("lead", "")] for pod, v in seed_data.POD_LEADS.items()]
        if rows:
            ws.append_rows(rows, value_input_option=RAW)


def _ws(name):
    return _spreadsheet().worksheet(name)


@st.cache_data(ttl=30)
def _records(name):
    return _ws(name).get_all_records()


def _flush():
    _records.clear()


# ---- Sessions ----
def get_sessions():
    out = []
    for r in _records("Sessions"):
        r = dict(r)
        r["id"] = str(r.get("id", ""))
        for c in SESSION_COLS:
            r[c] = str(r.get(c, ""))
        out.append(r)
    return out


def save_session(rec):
    ws = _ws("Sessions")
    recs = _records("Sessions")
    if rec.get("id"):
        for i, r in enumerate(recs):
            if str(r.get("id")) == str(rec["id"]):
                ws.update(range_name=f"A{i + 2}", values=[[str(rec.get(c, "")) for c in SESSION_COLS]],
                          value_input_option=RAW)
                _flush()
                return rec
    rec["id"] = rec.get("id") or uuid.uuid4().hex[:10]
    ws.append_row([str(rec.get(c, "")) for c in SESSION_COLS], value_input_option=RAW)
    _flush()
    return rec


def delete_session(sid):
    ws = _ws("Sessions")
    for i, r in enumerate(_records("Sessions")):
        if str(r.get("id")) == str(sid):
            ws.delete_rows(i + 2)
            break
    _flush()


def set_gcal_id(sid, gcal_id):
    ws = _ws("Sessions")
    col = SESSION_COLS.index("gcal_id") + 1
    for i, r in enumerate(_records("Sessions")):
        if str(r.get("id")) == str(sid):
            ws.update_cell(i + 2, col, gcal_id)
            break
    _flush()


# ---- Participants ----
def get_participants():
    d = {}
    for r in _records("Participants"):
        d.setdefault(str(r.get("pod", "")), []).append(str(r.get("email", "")))
    return d


def add_participant(pod, email):
    if email in get_participants().get(pod, []):
        return
    _ws("Participants").append_row([pod, email], value_input_option=RAW)
    _flush()


def remove_participant(pod, email):
    ws = _ws("Participants")
    for i, r in enumerate(_records("Participants")):
        if str(r.get("pod")) == pod and str(r.get("email")) == email:
            ws.delete_rows(i + 2)
            break
    _flush()


# ---- Pod leads ----
def get_pod_leads():
    d = {}
    for r in _records("PodLeads"):
        d[str(r.get("pod", ""))] = {"owner": str(r.get("owner", "")), "lead": str(r.get("lead", ""))}
    return d


def set_pod_lead(pod, field, email):
    ws = _ws("PodLeads")
    col = 2 if field == "owner" else 3
    for i, r in enumerate(_records("PodLeads")):
        if str(r.get("pod")) == pod:
            ws.update_cell(i + 2, col, email)
            _flush()
            return
    ws.append_row([pod, email if field == "owner" else "", email if field == "lead" else ""], value_input_option=RAW)
    _flush()


def invitees(pod):
    leads = get_pod_leads().get(pod, {})
    out = []
    for e in (leads.get("owner", ""), leads.get("lead", "")):
        if e and e not in out:
            out.append(e)
    for e in get_participants().get(pod, []):
        if e not in out:
            out.append(e)
    return out

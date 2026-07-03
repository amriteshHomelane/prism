"""Local JSON backend — single machine, zero setup. Used when Google Sheets
is not configured. Persists to data_store.json next to this file.
"""

import json
import os
import uuid

import seed_data

__all__ = ["get_sessions", "save_session", "delete_session", "set_gcal_id",
           "get_participants", "add_participant", "remove_participant",
           "get_pod_leads", "set_pod_lead", "invitees"]

_PATH = os.path.join(os.path.dirname(__file__), "data_store.json")


def _default():
    sessions = []
    for s in seed_data.SESSIONS:
        s = dict(s)
        s["id"] = uuid.uuid4().hex[:10]
        sessions.append(s)
    return {
        "sessions": sessions,
        "participants": {k: list(v) for k, v in seed_data.PARTICIPANTS.items()},
        "pod_leads": {k: dict(v) for k, v in seed_data.POD_LEADS.items()},
    }


def _read():
    if not os.path.exists(_PATH):
        data = _default()
        _write(data)
        return data
    with open(_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _write(data):
    with open(_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_sessions():
    return _read()["sessions"]


def save_session(rec):
    data = _read()
    if rec.get("id"):
        for i, s in enumerate(data["sessions"]):
            if s["id"] == rec["id"]:
                data["sessions"][i] = rec
                break
        else:
            data["sessions"].append(rec)
    else:
        rec["id"] = uuid.uuid4().hex[:10]
        data["sessions"].append(rec)
    _write(data)
    return rec


def delete_session(sid):
    data = _read()
    data["sessions"] = [s for s in data["sessions"] if s["id"] != sid]
    _write(data)


def set_gcal_id(sid, gcal_id):
    data = _read()
    for s in data["sessions"]:
        if s["id"] == sid:
            s["gcal_id"] = gcal_id
    _write(data)


def get_participants():
    return _read()["participants"]


def add_participant(pod, email):
    data = _read()
    data["participants"].setdefault(pod, [])
    if email not in data["participants"][pod]:
        data["participants"][pod].append(email)
    _write(data)


def remove_participant(pod, email):
    data = _read()
    data["participants"][pod] = [e for e in data["participants"].get(pod, []) if e != email]
    _write(data)


def get_pod_leads():
    return _read()["pod_leads"]


def set_pod_lead(pod, field, email):
    data = _read()
    data["pod_leads"].setdefault(pod, {"owner": "", "lead": ""})
    data["pod_leads"][pod][field] = email
    _write(data)


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

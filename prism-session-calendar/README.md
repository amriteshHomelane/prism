# Prism Academy — Session Calendar (Streamlit)

A month-on-month training calendar for Prism Academy programs (pods). Pod owners
schedule faculty sessions; a program admin oversees everything; participants get
invited on Google Calendar sync. Built to validate the tool first, then port into
MyHQ later.

## Step 1 — Check it locally (no Google setup needed)

```bash
cd prism-session-calendar
python -m venv .venv && source .venv/bin/activate     # optional
pip install -r requirements.txt
streamlit run app.py
```

Opens at http://localhost:8501. Data seeds from `seed_data.py` into
`data_store.json` (delete that file to reset). You can:

- Browse the month calendar (opens on June 2026, where the data starts)
- Switch **Preview as**: Program admin / Pod owner / Others (role simulator)
- Add / edit / delete sessions, manage participants
- As **Program admin**, reassign pod owner + content lead
- **Export .ics** and import it into Google Calendar right away

Everything works offline at this stage — this is the version to share and validate.

## Step 2 — Turn on live Google Calendar sync

1. In Google Cloud: create a project, enable **Google Calendar API**.
2. Create a **Service Account**, download its JSON key.
3. Create a shared calendar ("Prism Academy") and share it with the service
   account email (Make changes to events).
4. To send invitations to participants (HomeLane + Design Cafe), have a Workspace
   admin enable **domain-wide delegation** for the service account with scope
   `https://www.googleapis.com/auth/calendar`.
5. `cp .streamlit/secrets.toml.example .streamlit/secrets.toml` and fill in the
   service-account fields, `calendar_id`, and `impersonate`.

Restart the app: the **Sync to Google Calendar** button now creates/updates events
with attendees. Each event's id is saved back onto the session, so re-syncing
**updates** events instead of duplicating them.

## Step 3 — Shared data (multi-user)  ✅ built in

The app auto-selects its backend:

- **Local file** (`backend_local.py` → `data_store.json`) when Sheets isn't configured.
- **Google Sheets** (`backend_sheets.py`) when it is — shared, persistent, multi-user.

To switch on Google Sheets:

1. Create a Google Sheet (any blank one).
2. Share it with the **service-account client_email** (from `[gcp_service_account]`) as **Editor**.
3. Copy the sheet ID (the string in the URL between `/d/` and `/edit`) into
   `[sheets].sheet_id` in `secrets.toml`.

On first load the app creates three tabs — `Sessions`, `Participants`, `PodLeads` —
and seeds them from `seed_data.py`. After that, every edit reads/writes the sheet,
so all users share one source of truth and edits persist across restarts. The
sidebar shows which backend is active. (This is also what makes edits stick on
Streamlit Community Cloud, whose local disk is ephemeral.)

## Step 4 — Real login + roles

Swap the sidebar "Preview as" radio in `app.py` for Streamlit's native auth:

```python
if not st.user.is_logged_in:
    st.button("Sign in", on_click=st.login); st.stop()
role = resolve_role(st.user.email)
```

Configure a Google OIDC provider in `secrets.toml` and restrict to homelane.com /
designcafe.com. `resolve_role()` already maps email → admin / pod owner / others.

## Step 5 — Deploy / port to MyHQ

- **Interim host:** internal container or Streamlit with the OIDC gate on
  (avoid unauthenticated public hosting — participant emails are internal PII).
- **Long term:** rebuild the UI as a **MyHQ plugin** (React micro-frontend). The
  `calendar_sync` logic and data model carry straight over; MyHQ provides login,
  identity → role, and hosting.

## Files

| File | Purpose |
|---|---|
| `app.py` | Streamlit UI (calendar, sessions, participants, roles) |
| `store.py` | Local JSON persistence (swap for Google Sheets in Step 3) |
| `calendar_sync.py` | Google Calendar upsert + `.ics` fallback |
| `seed_data.py` | Real Dovetail + Advanced (Sr. DC) data, pods, faculty, participants |

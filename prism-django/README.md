# Prism Academy — Session Calendar (Django)

A hostable, multi-user session calendar for Prism Academy programs (pods), on
HomeLane's approved stack (Django). Engineering owns hosting; the data model
matches the Streamlit prototype and the eventual MyHQ plugin.

**What's included**
- Data models: `Pod`, `Session`, `Participant` (+ owner/content-lead on each pod)
- **Django admin** — full multi-user editing with real logins & permissions
- **REST API** (Django REST Framework) for any frontend (e.g. the MyHQ React plugin)
- **Google Calendar sync** — per-session + bulk admin action + `.ics` export
- **Seed command** with all real data (3 pods live, 3 placeholders)
- Brand-styled read-only **calendar page** at `/`

## Run locally

```bash
cd prism-django
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_prism            # loads pods, participants, sessions
python manage.py createsuperuser       # your admin login
python manage.py runserver
```

- Calendar view: http://127.0.0.1:8000/
- Admin (edit everything): http://127.0.0.1:8000/admin/
- API root: http://127.0.0.1:8000/api/

## REST API

| Endpoint | Use |
|---|---|
| `GET/POST /api/sessions/` | list / create sessions |
| `GET/PUT/PATCH/DELETE /api/sessions/{id}/` | read / edit / delete |
| `POST /api/sessions/{id}/sync/` | push one session to Google Calendar |
| `GET /api/sessions/ics/?pod=Dovetail` | download `.ics` (optionally per pod) |
| `/api/pods/`, `/api/participants/` | pods (with invitee lists) & participants |

## Google Calendar sync (optional)

Set these environment variables, then use **Admin → Sessions → “Sync selected
sessions to Google Calendar”** (or `POST /api/sessions/{id}/sync/`):

```bash
export GOOGLE_SA_JSON=/path/to/service-account.json
export GOOGLE_CALENDAR_ID="c_xxxx@group.calendar.google.com"
export GOOGLE_IMPERSONATE="pavithra.s@homelane.com"   # domain-wide delegation (sends invites)
```

Share the target calendar with the service-account email. Each event's id is
stored on the session, so re-syncing **updates** (never duplicates).

## Production notes for engineering

- **Lock down the API.** The scaffold uses `AllowAny` so it runs out of the box.
  Switch `REST_FRAMEWORK` to `IsAuthenticatedOrReadOnly` and wire HomeLane SSO
  (map email → role: admin = `PRISM_ADMIN_EMAIL`, pod owners = pod owner/lead
  emails, others = read).
- **Config via env:** `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=false`,
  `DJANGO_ALLOWED_HOSTS`, `DJANGO_CSRF_TRUSTED_ORIGINS`, and `POSTGRES_*` for a
  real database. `collectstatic` + `gunicorn prism.wsgi` behind your proxy.
- **Roles / editing:** the Django admin already gives permissioned multi-user
  editing today. The polished pod-owner UI (from the prototype) can be layered
  on the REST API, or becomes the MyHQ React plugin — same endpoints.

## Layout

```
prism/            settings, urls, wsgi/asgi
calendar_app/
  models.py       Pod / Session / Participant
  admin.py        admin UI + Google Calendar sync action
  serializers.py  DRF serializers
  views.py        API viewsets + calendar page
  urls.py         router
  gcal.py         Google Calendar upsert + .ics
  seed_data.py    real data
  management/commands/seed_prism.py
  templates/calendar_app/index.html   calendar page
```

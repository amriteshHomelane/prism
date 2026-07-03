"""Load pods, participants and sessions from calendar_app/seed_data.py.

    python manage.py seed_prism

Pods and participants are upserted every run (safe to re-run). Sessions are
loaded only when the Session table is empty, so it won't clobber later edits.
Pass --reset-sessions to wipe and reload sessions from seed.
"""

import datetime

from django.core.management.base import BaseCommand

from calendar_app import seed_data
from calendar_app.models import Participant, Pod, Session


class Command(BaseCommand):
    help = "Seed the database with Prism pods, participants and sessions."

    def add_arguments(self, parser):
        parser.add_argument("--reset-sessions", action="store_true",
                            help="Delete existing sessions and reload them from seed.")

    def handle(self, *args, **opts):
        for i, p in enumerate(seed_data.PODS):
            leads = seed_data.POD_LEADS.get(p["short"], {})
            Pod.objects.update_or_create(
                short=p["short"],
                defaults={"name": p["name"], "color": p["color"], "order": i,
                          "owner_email": leads.get("owner", ""), "lead_email": leads.get("lead", "")},
            )
        pods = {p.short: p for p in Pod.objects.all()}

        added_p = 0
        for short, emails in seed_data.PARTICIPANTS.items():
            pod = pods.get(short)
            if not pod:
                continue
            for email in emails:
                _, created = Participant.objects.get_or_create(pod=pod, email=email)
                added_p += int(created)

        if opts["reset_sessions"]:
            Session.objects.all().delete()
        added_s = 0
        if Session.objects.count() == 0:
            for s in seed_data.SESSIONS:
                pod = pods.get(s["pod"])
                if not pod:
                    continue
                Session.objects.create(
                    pod=pod, type=s["type"], title=s["title"], faculty=s["faculty"], fkind=s["fkind"],
                    date=datetime.date.fromisoformat(s["date"]), start=s["start"], end=s["end"],
                    status=s["status"], mode=s["mode"], loc=s.get("loc", ""), note=s.get("note", ""),
                )
                added_s += 1
        else:
            self.stdout.write("Sessions already present — skipped (use --reset-sessions to reload).")

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {Pod.objects.count()} pods, +{added_p} participants, +{added_s} sessions."))

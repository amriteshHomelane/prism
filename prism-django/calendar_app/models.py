from django.db import models


class Pod(models.Model):
    """A Prism program. `short` is the display key; `name` is the full title."""
    short = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=9, default="#4A6741")
    owner_email = models.EmailField(blank=True)
    lead_email = models.EmailField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "short"]

    def __str__(self):
        return self.short

    def invitees(self):
        """Owner + content lead + participants (deduped) — the Google Calendar invite list."""
        out = []
        for e in (self.owner_email, self.lead_email):
            if e and e not in out:
                out.append(e)
        for p in self.participants.all():
            if p.email not in out:
                out.append(p.email)
        return out


class Session(models.Model):
    TYPE = [("module", "Module"), ("fireside", "Fireside"),
            ("assessment", "Assessment"), ("activity", "Activity")]
    MODE = [("virtual", "Virtual"), ("inperson", "In person")]
    STATUS = [("proposed", "Proposed"), ("confirmed", "Confirmed")]
    FKIND = [("internal", "Internal"), ("external", "External")]

    pod = models.ForeignKey(Pod, on_delete=models.CASCADE, related_name="sessions")
    type = models.CharField(max_length=20, choices=TYPE, default="module")
    title = models.CharField(max_length=255)
    faculty = models.CharField(max_length=255, blank=True)
    fkind = models.CharField(max_length=10, choices=FKIND, default="internal")
    date = models.DateField()
    start = models.CharField(max_length=5, help_text="HH:MM (24h)")
    end = models.CharField(max_length=5, blank=True, help_text="HH:MM (24h)")
    status = models.CharField(max_length=10, choices=STATUS, default="proposed")
    mode = models.CharField(max_length=10, choices=MODE, default="virtual")
    loc = models.CharField(max_length=500, blank=True, help_text="Venue or meeting link")
    note = models.TextField(blank=True)
    gcal_id = models.CharField(max_length=255, blank=True, help_text="Google Calendar event id (set on sync)")

    class Meta:
        ordering = ["date", "start"]

    def __str__(self):
        return f"{self.date} {self.title} ({self.pod.short})"


class Participant(models.Model):
    pod = models.ForeignKey(Pod, on_delete=models.CASCADE, related_name="participants")
    email = models.EmailField()

    class Meta:
        unique_together = ("pod", "email")
        ordering = ["email"]

    def __str__(self):
        return f"{self.email} [{self.pod.short}]"

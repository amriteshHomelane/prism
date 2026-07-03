from django.contrib import admin, messages

from . import gcal
from .models import Participant, Pod, Session


@admin.action(description="Sync selected sessions to Google Calendar")
def sync_selected(modeladmin, request, queryset):
    if not gcal.is_configured():
        modeladmin.message_user(request, "Google Calendar is not configured (set GOOGLE_SA_JSON and GOOGLE_CALENDAR_ID).", messages.WARNING)
        return
    ok = 0
    for s in queryset:
        try:
            s.gcal_id = gcal.upsert_event(s, s.pod.invitees())
            s.save(update_fields=["gcal_id"])
            ok += 1
        except Exception as exc:  # noqa: BLE001
            modeladmin.message_user(request, f"{s.title}: {exc}", messages.ERROR)
    if ok:
        modeladmin.message_user(request, f"Synced {ok} session(s) to Google Calendar.")


class ParticipantInline(admin.TabularInline):
    model = Participant
    extra = 1


@admin.register(Pod)
class PodAdmin(admin.ModelAdmin):
    list_display = ["short", "name", "owner_email", "lead_email", "participant_count"]
    search_fields = ["short", "name"]
    inlines = [ParticipantInline]

    @admin.display(description="Participants")
    def participant_count(self, obj):
        return obj.participants.count()


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ["date", "start", "title", "pod", "type", "faculty", "mode", "status"]
    list_filter = ["pod", "type", "mode", "status", "fkind"]
    search_fields = ["title", "faculty"]
    date_hierarchy = "date"
    list_editable = ["status"]
    actions = [sync_selected]


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ["email", "pod"]
    list_filter = ["pod"]
    search_fields = ["email"]

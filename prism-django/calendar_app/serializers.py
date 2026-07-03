from rest_framework import serializers

from .models import Participant, Pod, Session


class PodSerializer(serializers.ModelSerializer):
    participant_count = serializers.IntegerField(source="participants.count", read_only=True)
    invitees = serializers.SerializerMethodField()

    class Meta:
        model = Pod
        fields = ["id", "short", "name", "color", "owner_email", "lead_email", "order",
                  "participant_count", "invitees"]

    def get_invitees(self, obj):
        return obj.invitees()


class SessionSerializer(serializers.ModelSerializer):
    pod_short = serializers.CharField(source="pod.short", read_only=True)
    pod_name = serializers.CharField(source="pod.name", read_only=True)
    pod_color = serializers.CharField(source="pod.color", read_only=True)

    class Meta:
        model = Session
        fields = ["id", "pod", "pod_short", "pod_name", "pod_color", "type", "title",
                  "faculty", "fkind", "date", "start", "end", "status", "mode", "loc",
                  "note", "gcal_id"]


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ["id", "pod", "email"]

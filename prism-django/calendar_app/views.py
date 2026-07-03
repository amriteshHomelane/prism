from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from . import gcal
from .models import Participant, Pod, Session
from .serializers import ParticipantSerializer, PodSerializer, SessionSerializer


def index(request):
    return render(request, "calendar_app/index.html", {
        "admin_email": settings.PRISM_ADMIN_EMAIL,
        "gcal_configured": gcal.is_configured(),
    })


class PodViewSet(viewsets.ModelViewSet):
    queryset = Pod.objects.all()
    serializer_class = PodSerializer


class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.select_related("pod").all()
    serializer_class = ParticipantSerializer


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.select_related("pod").all()
    serializer_class = SessionSerializer

    @action(detail=True, methods=["post"])
    def sync(self, request, pk=None):
        """Push this session to Google Calendar."""
        if not gcal.is_configured():
            return Response({"detail": "Google Calendar not configured."}, status=400)
        s = self.get_object()
        s.gcal_id = gcal.upsert_event(s, s.pod.invitees())
        s.save(update_fields=["gcal_id"])
        return Response({"gcal_id": s.gcal_id})

    @action(detail=False, methods=["get"])
    def ics(self, request):
        """Download all (optionally ?pod=Short) sessions as an .ics file."""
        qs = self.get_queryset()
        pod = request.query_params.get("pod")
        if pod:
            qs = qs.filter(pod__short=pod)
        resp = HttpResponse(gcal.build_ics(qs), content_type="text/calendar")
        resp["Content-Disposition"] = 'attachment; filename="prism-sessions.ics"'
        return resp

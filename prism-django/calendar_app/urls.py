from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("pods", views.PodViewSet)
router.register("sessions", views.SessionViewSet)
router.register("participants", views.ParticipantViewSet)

urlpatterns = [
    path("", views.index, name="index"),
    path("api/", include(router.urls)),
]

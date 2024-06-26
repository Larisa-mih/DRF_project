from django.urls import path
from rest_framework.routers import DefaultRouter

from materials.apps import MaterialsConfig
from materials.views import (
    CourseViewSet,
    SubjectCreateAPIView,
    SubjectDestroyAPIView,
    SubjectListAPIView,
    SubjectRetrieveAPIView,
    SubjectUpdateAPIView,
    SubscriptionCreateView,
)

app_name = MaterialsConfig.name

router = DefaultRouter()
router.register(r"course", CourseViewSet, basename="course")

urlpatterns = [
    path("subject/create", SubjectCreateAPIView.as_view(), name="subjects_create"),
    path("subject/", SubjectListAPIView.as_view(), name="subjects_list"),
    path(
        "subject/detail/<int:pk>",
        SubjectRetrieveAPIView.as_view(),
        name="subjects_detail",
    ),
    path("subject/edit/<int:pk>", SubjectUpdateAPIView.as_view(), name="subjects_edit"),
    path(
        "subject/delete/<int:pk>",
        SubjectDestroyAPIView.as_view(),
        name="subjects_delete",
    ),
    path(
        "subscription/create",
        SubscriptionCreateView.as_view(),
        name="subscription_create",
    ),
] + router.urls

from django.urls import path

from . import views

urlpatterns = [
    path("projects/", views.ProjectListView.as_view(), name="project-list"),
    path(
        "projects/<slug:slug>/",
        views.ProjectDetailView.as_view(),
        name="project-detail",
    ),
    path("contact/", views.ContactCreateView.as_view(), name="contact-create"),
    path("health/", views.health_check, name="health-check"),
]

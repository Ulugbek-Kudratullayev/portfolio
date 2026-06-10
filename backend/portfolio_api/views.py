from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from .models import Project
from .serializers import ContactMessageSerializer, ProjectSerializer


class ProjectListView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    filterset_fields = ["category", "platform", "is_featured"]
    search_fields = ["title", "description_en", "description_uz", "tech_stack_raw"]
    ordering_fields = ["order", "title", "created_at"]

    def get_queryset(self):
        queryset = Project.objects.filter(is_published=True)
        if self.request.query_params.get("featured") in ("true", "1"):
            queryset = queryset.filter(is_featured=True)
        return queryset


class ProjectDetailView(generics.RetrieveAPIView):
    serializer_class = ProjectSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return Project.objects.filter(is_published=True)


class ContactThrottle(AnonRateThrottle):
    scope = "contact"


class ContactCreateView(generics.CreateAPIView):
    serializer_class = ContactMessageSerializer
    throttle_classes = [ContactThrottle]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"success": True, "detail": "Message received. Thank you!"},
            status=status.HTTP_201_CREATED,
        )


def health_check(request):
    return JsonResponse({"status": "ok"})

from rest_framework import serializers

from .models import ContactMessage, Project


class ProjectSerializer(serializers.ModelSerializer):
    cover_image = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "slug",
            "title",
            "category",
            "platform",
            "description_en",
            "description_uz",
            "tech_stack",
            "tech_stack_raw",
            "features",
            "cover_image",
            "screenshots",
            "live_url",
            "github_url",
            "is_featured",
            "order",
        ]

    def get_cover_image(self, obj: Project) -> str | None:
        if not obj.cover_image:
            return None
        request = self.context.get("request")
        url = obj.cover_image.url
        return request.build_absolute_uri(url) if request else url


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ["full_name", "email", "message"]

    def validate_message(self, value: str) -> str:
        cleaned = value.strip()
        if len(cleaned) < 10:
            raise serializers.ValidationError(
                "Message is too short (minimum 10 characters)."
            )
        return cleaned

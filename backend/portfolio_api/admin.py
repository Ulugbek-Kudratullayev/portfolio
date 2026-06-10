from django.contrib import admin

from .models import ContactMessage, Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "platform",
        "is_featured",
        "is_published",
        "order",
    )
    list_filter = ("is_featured", "is_published", "platform", "category")
    list_editable = ("is_featured", "is_published", "order")
    search_fields = ("title", "slug", "description_en", "description_uz")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "created_at", "is_read")
    list_filter = ("is_read",)
    readonly_fields = ("full_name", "email", "message", "created_at")

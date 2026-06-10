from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from unfold.decorators import action, display
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from .models import ContactMessage, Project

admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


@admin.register(Project)
class ProjectAdmin(ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    list_fullwidth = True

    list_display = (
        "title",
        "category",
        "platform_badge",
        "featured_badge",
        "is_published",
        "order",
    )
    list_editable = ("is_published", "order")
    list_filter = ("is_featured", "is_published", "platform", "category")
    search_fields = ("title", "slug", "description_en", "description_uz")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("order", "title")
    actions = ("make_featured", "remove_featured")

    fieldsets = (
        (
            _("Asosiy"),
            {
                "fields": (
                    ("title", "slug"),
                    ("category", "platform"),
                    ("is_featured", "is_published", "order"),
                )
            },
        ),
        (
            _("Tavsif"),
            {"fields": ("description_en", "description_uz", "features")},
        ),
        (
            _("Texnologiyalar"),
            {"fields": ("tech_stack", "tech_stack_raw")},
        ),
        (
            _("Media va havolalar"),
            {"fields": ("cover_image", "screenshots", "live_url", "github_url")},
        ),
    )

    @display(
        description=_("Platforma"),
        label={
            Project.Platform.WEB: "info",
            Project.Platform.MOBILE: "success",
            Project.Platform.DESKTOP: "warning",
            Project.Platform.BOT: "info",
            Project.Platform.CLI: "danger",
            Project.Platform.FULLSTACK: "success",
        },
    )
    def platform_badge(self, obj):
        return obj.platform

    @display(
        description=_("Featured"),
        label={"Featured": "success"},
    )
    def featured_badge(self, obj):
        return "Featured" if obj.is_featured else "—"

    @action(description=_("Tanlanganlarni featured qilish"))
    def make_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f"{updated} ta loyiha featured qilindi.")

    @action(description=_("Featured belgisini olib tashlash"))
    def remove_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(
            request, f"{updated} ta loyihadan featured olib tashlandi."
        )


@admin.register(ContactMessage)
class ContactMessageAdmin(ModelAdmin):
    list_fullwidth = True

    list_display = (
        "full_name",
        "email",
        "short_message",
        "created_at",
        "status_badge",
    )
    list_filter = ("is_read",)
    search_fields = ("full_name", "email", "message")
    readonly_fields = ("full_name", "email", "message", "created_at")
    actions = ("mark_read", "mark_unread")
    date_hierarchy = "created_at"

    @display(description=_("Xabar"))
    def short_message(self, obj):
        if len(obj.message) > 80:
            return f"{obj.message[:80]}…"
        return obj.message

    @display(
        description=_("Holat"),
        label={"Yangi": "danger", "O'qilgan": "success"},
    )
    def status_badge(self, obj):
        return "O'qilgan" if obj.is_read else "Yangi"

    @action(description=_("O'qilgan deb belgilash"))
    def mark_read(self, request, queryset):
        queryset.update(is_read=True)

    @action(description=_("O'qilmagan deb belgilash"))
    def mark_unread(self, request, queryset):
        queryset.update(is_read=False)

    def has_add_permission(self, request):
        return False

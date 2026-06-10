from django.db import models


class Project(models.Model):
    """A portfolio project, seeded from local project scans and editable in admin."""

    class Platform(models.TextChoices):
        WEB = "web", "Web"
        MOBILE = "mobile", "Mobile"
        DESKTOP = "desktop", "Desktop"
        BOT = "bot", "Bot"
        CLI = "cli", "CLI"
        FULLSTACK = "fullstack", "Web + Mobile"

    slug = models.SlugField(max_length=120, unique=True)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=120)
    platform = models.CharField(
        max_length=20, choices=Platform.choices, default=Platform.WEB
    )

    description_en = models.TextField(blank=True)
    description_uz = models.TextField(blank=True)

    # Normalized tech keys the frontend maps to icons, e.g. ["django", "react"].
    tech_stack = models.JSONField(default=list, blank=True)
    # Raw human-readable stack, e.g. "Django 5, React 18, PostgreSQL".
    tech_stack_raw = models.CharField(max_length=500, blank=True)
    # Key features, list of short strings.
    features = models.JSONField(default=list, blank=True)

    cover_image = models.ImageField(upload_to="covers/", blank=True, null=True)
    # Optional external/static screenshot URLs.
    screenshots = models.JSONField(default=list, blank=True)

    live_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)

    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "title"]

    def __str__(self) -> str:
        return self.title


class ContactMessage(models.Model):
    """Messages submitted through the portfolio contact form."""

    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.full_name} <{self.email}>"

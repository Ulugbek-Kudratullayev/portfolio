"""Callbacks used by the Unfold admin theme (referenced from settings.UNFOLD)."""

import os


def environment_callback(request):
    """Show which environment the admin is running in (top-right badge)."""
    if os.environ.get("RAILWAY_ENVIRONMENT"):
        return ["Production", "danger"]
    return ["Local", "info"]


def unread_messages_badge(request):
    """Unread contact message count shown next to the sidebar item."""
    from portfolio_api.models import ContactMessage

    count = ContactMessage.objects.filter(is_read=False).count()
    return count if count else None

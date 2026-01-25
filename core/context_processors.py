from .models import SupportMessage


def admin_message_count(request):
    """
    Context processor to add unresolved message count for admin users.
    This count will be available in all templates for displaying in the sidebar badge.
    """
    context = {}
    
    if request.user.is_authenticated and request.user.is_superuser:
        # Count unresolved support messages for admin users
        unresolved_count = SupportMessage.objects.filter(is_resolved=False).count()
        context['unresolved_message_count'] = unresolved_count if unresolved_count > 0 else None
    
    return context

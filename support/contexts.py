"""Support app's context"""
from .models import CustomerSuport, Message


def message_context(request):
    """
    Support app's context
    Check current user messages
    Return all the messages for user
    If admin return all the messages
    Count all the unread messages
    And finaly returrn to context
    """
    unread_messages_count = 0
    user_messages = None
    all_messages = Message.objects.all()

    if request.user.is_authenticated:
        profile = request.user
        user_messages = []
        if not request.user.is_superuser:
            if all_messages:
                issues = profile.user_support.all().exclude(status='Resolved')
        else:
            issues = CustomerSuport.objects.all()

        filtered_mesages = all_messages.exclude(
            user=profile).exclude(unread=False)

        for i in filtered_mesages:
            if i.thread in issues:
                unread_messages_count += 1
                user_messages.append({
                    'user': i.user.username,
                    'thread': i.thread,
                    'message': i.message,
                    'timestamp': i.timestamp,
                })

    context = {
        'unread_messages_count': unread_messages_count,
        'user_messages': user_messages,
    }

    return context

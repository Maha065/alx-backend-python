from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from messaging.models import Message
from django.contrib.auth.models import User


@login_required
@cache_page(60)  # cache for 60 seconds
def conversation_view(request, user_id):
    """
    Display conversation between logged-in user and another user,
    cached for 60 seconds.
    """
    other_user = get_object_or_404(User, id=user_id)

    # Fetch conversation (both directions)
    messages = (
        Message.objects.filter(
            sender__in=[request.user, other_user],
            receiver__in=[request.user, other_user],
        )
        .select_related("sender", "receiver")
        .order_by("timestamp")
    )

    return render(request, "chats/conversation.html", {
        "messages": messages,
        "other_user": other_user,
    })

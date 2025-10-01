from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message


@login_required
def inbox(request):
    """Display only unread messages for the logged-in user"""
    unread_messages = Message.unread.for_user(request.user)
    return render(request, "messaging/inbox.html", {"unread_messages": unread_messages})

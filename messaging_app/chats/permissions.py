# messaging_app/chats/permissions.py
from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Ensure users only access their own messages or conversations.
    """

    def has_object_permission(self, request, view, obj):
        # If it's a message (assume Message has sender field)
        if hasattr(obj, "sender"):
            return obj.sender == request.user
        # If it's a conversation (assume Conversation has participants m2m)
        if hasattr(obj, "participants"):
            return request.user in obj.participants.all()
        return False

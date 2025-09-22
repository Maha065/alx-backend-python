# messaging_app/chats/permissions.py
from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Object-level permission to only allow owners to access their own messages/conversations.
    """

    def has_object_permission(self, request, view, obj):
        # Assuming Message has `sender` and Conversation has `participants`
        if hasattr(obj, 'sender'):
            return obj.sender == request.user
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        return False

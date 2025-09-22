# messaging_app/chats/permissions.py
from rest_framework.permissions import BasePermission, IsAuthenticated

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission:
    - Only authenticated users
    - Only participants in a conversation can interact with its messages
    """

    def has_permission(self, request, view):
        # First ensure the user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        obj can be a Message or a Conversation.
        - For Message: check if request.user is in obj.conversation.participants
        - For Conversation: check if request.user is in obj.participants
        """
        if hasattr(obj, "conversation"):  # Message object
            return request.user in obj.conversation.participants.all()
        if hasattr(obj, "participants"):  # Conversation object
            return request.user in obj.participants.all()
        return False

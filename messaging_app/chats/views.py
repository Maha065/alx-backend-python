# messaging_app/chats/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .permissions import IsParticipantOfConversation
from .models import Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        # Only return conversations the user is part of
        return Conversation.objects.filter(participants=self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        # Only return messages from conversations the user is part of
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        # Ensure message is tied to a conversation the user belongs to
        conversation = serializer.validated_data.get("conversation")
        if self.request.user in conversation.participants.all():
            serializer.save(sender=self.request.user)
        else:
            raise PermissionDenied("You are not a participant of this conversation.")

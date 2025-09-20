class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().order_by("-created_at")
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        # creates a conversation with participants
        ...
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by("sent_at")
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        # creates a message in a conversation
        ...
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from chats.views import ConversationViewSet, MessageViewSet

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('api/', include(router.urls)),
]
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('chats.urls')),  # ensure this line exists
]

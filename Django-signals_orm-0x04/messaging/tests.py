from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory


class MessagingSignalTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username="alice", password="password123")
        self.receiver = User.objects.create_user(username="bob", password="password123")

    def test_notification_created_on_message(self):
        msg = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Hello Bob!"
        )
        self.assertEqual(Notification.objects.count(), 1)

    def test_message_edit_creates_history(self):
        msg = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Original Message"
        )
        msg.content = "Edited Message"
        msg.save()

        history = MessageHistory.objects.filter(message=msg)
        self.assertEqual(history.count(), 1)
        self.assertEqual(history.first().old_content, "Original Message")
        self.assertTrue(msg.edited)

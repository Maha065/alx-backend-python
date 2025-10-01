from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory


class UserDeletionTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="alice", password="pass123")
        self.user2 = User.objects.create_user(username="bob", password="pass123")

    def test_user_deletion_cleans_related_data(self):
        # Create a message and notification
        msg = Message.objects.create(sender=self.user1, receiver=self.user2, content="Hi Bob")
        msg.content = "Edited Hi Bob"
        msg.save()  # creates MessageHistory

        # Ensure objects exist
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(Notification.objects.count(), 1)
        self.assertEqual(MessageHistory.objects.count(), 1)

        # Delete user1
        self.user1.delete()

        # Related data should be deleted
        self.assertEqual(Message.objects.count(), 0)
        self.assertEqual(Notification.objects.count(), 0)
        self.assertEqual(MessageHistory.objects.count(), 0)

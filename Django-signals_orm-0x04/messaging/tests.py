from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message


class UnreadMessagesManagerTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="alice", password="pass123")
        self.user2 = User.objects.create_user(username="bob", password="pass123")

    def test_unread_messages_for_user(self):
        # One unread message
        msg1 = Message.objects.create(sender=self.user1, receiver=self.user2, content="Hello Bob!", read=False)
        # One read message
        msg2 = Message.objects.create(sender=self.user1, receiver=self.user2, content="This is read", read=True)

        unread_msgs = Message.unread.for_user(self.user2)

        self.assertEqual(unread_msgs.count(), 1)
        self.assertEqual(unread_msgs.first(), msg1)

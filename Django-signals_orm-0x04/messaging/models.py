from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)

    # New field: reply threading
    parent_message = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies"
    )

    def __str__(self):
        if self.parent_message:
            return f"Reply by {self.sender} to Message {self.parent_message.id}"
        return f"Message from {self.sender} to {self.receiver}"

    def get_thread(self):
        """
        Recursively fetch all replies to this message in threaded format.
        """
        thread = []
        for reply in self.replies.a


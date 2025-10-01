from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    """Create a Notification whenever a new Message is created"""
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """Log old content before a message is updated"""
    if instance.pk:  # means message already exists
        try:
            old_instance = Message.objects.get(pk=instance.pk)
        except Message.DoesNotExist:
            return

        if old_instance.content != instance.content:  # content is changing
            MessageHistory.objects.create(
                message=instance,
                old_content=old_instance.content
            )
            instance.edited = True  # mark as edited

# messaging_app/chats/filters.py
import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    # Filter by user (sender id or username if related)
    sender = django_filters.NumberFilter(field_name="sender__id")
    # Time range filters
    start_date = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr="gte")
    end_date = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr="lte")

    class Meta:
        model = Message
        fields = ["sender", "start_date", "end_date"]

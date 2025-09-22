# messaging_app/chats/pagination.py
from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"  # allow client override (optional)
    max_page_size = 100

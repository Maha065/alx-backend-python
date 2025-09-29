import time
from django.http import HttpResponseForbidden
from collections import defaultdict, deque


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Store timestamps of POST requests per IP
        self.ip_requests = defaultdict(deque)
        self.limit = 5         # max messages
        self.window = 60       # time window in seconds (1 minute)

    def __call__(self, request):
        # Only check for POST requests (sending messages)
        if request.method == "POST":
            ip = self.get_client_ip(request)
            now = time.time()

            # Remove timestamps older than 1 minute
            while self.ip_requests[ip] and now - self.ip_requests[ip][0] > self.window:
                self.ip_requests[ip].popleft()

            # Check if user exceeds limit
            if len(self.ip_requests[ip]) >= self.limit:
                return HttpResponseForbidden(
                    "<h1>403 Forbidden</h1><p>Too many messages sent. Please wait before sending more.</p>"
                )

            # Add current timestamp
            self.ip_requests[ip].append(now)

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Extract client IP address from request headers"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR", "")
        return ip
from django.http import HttpResponseForbidden


class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)

        # Check if user is authenticated and has the right role
        if user and user.is_authenticated:
            # Example: allow if superuser or staff (you can adapt to a custom role field)
            if user.is_superuser or user.is_staff:
                return self.get_response(request)

            # If user model has a custom "role" field, check it
            role = getattr(user, "role", None)
            if role in ["admin", "moderator"]:
                return self.get_response(request)

            # Block others
            return HttpResponseForbidden(
                "<h1>403 Forbidden</h1><p>You do not have permission to perform this action.</p>"
            )

        # If user is not logged in, block access
        return HttpResponseForbidden(
            "<h1>403 Forbidden</h1><p>Authentication required.</p>"
        )

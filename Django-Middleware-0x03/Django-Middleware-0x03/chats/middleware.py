from datetime import datetime
from django.http import HttpResponseForbidden


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        # Deny access if time is outside 6AM - 9PM
        if current_hour < 6 or current_hour >= 21:
            return HttpResponseForbidden(
                "<h1>403 Forbidden</h1><p>Access to the chat is restricted during this time.</p>"
            )

        response = self.get_response(request)
        return response

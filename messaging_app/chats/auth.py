# messaging_app/chats/auth.py
from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    """
    Extend JWTAuthentication if you want custom behavior,
    e.g., logging or token validation tweaks.
    """
    pass

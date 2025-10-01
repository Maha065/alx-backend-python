from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, logout
from django.http import HttpResponse

User = get_user_model()


@login_required
def delete_user(request):
    """Allow the logged-in user to delete their account"""
    user = request.user
    logout(request)  # log out before deletion
    user.delete()
    return HttpResponse("Your account and related data have been deleted successfully.")

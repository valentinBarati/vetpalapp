from functools import wraps
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages

def check_user_permission(required_permission):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.has_perm(required_permission):
                messages.error(request, f"You are not allowed to view this page.")
                return redirect("home")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

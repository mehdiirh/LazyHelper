from django.core.exceptions import PermissionDenied
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import reverse

from functools import wraps

from utils.api.tools import user_security_check
from utils.core.exceptions import AuthenticationError


def login_required(redirect_login=False, next_redirect=None):

    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            try:
                user_security_check(request)
            except AuthenticationError:
                if not redirect_login:
                    raise PermissionDenied

                try:
                    next_redirect_url = reverse(next_redirect)
                except:
                    next_redirect_url = next_redirect

                print(next_redirect)
                return redirect_to_login(next_redirect_url, login_url='admin:login')

            return func(request, *args, **kwargs)

        return inner
    return decorator

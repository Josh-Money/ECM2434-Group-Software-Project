from django.shortcuts import redirect

class RedirectLoggedOutUsersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allowed paths for unauthenticated users
        allowed_paths = ['/', '/sign-up/', '/privacy-policy/']

        # If user is not authenticated and trying to access a restricted page, redirect them
        if request.path not in allowed_paths and not request.user.is_authenticated:
            return redirect('/login/')  # Redirect to login instead of home

        return self.get_response(request)


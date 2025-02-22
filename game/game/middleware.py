from django.shortcuts import redirect

class RedirectLoggedOutUsersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allowed paths for unauthenticated users
        allowed_paths = ['/', 'privacy-policy']

        # Check if the user is unauthenticated and accessing a restricted page
        if request.path not in allowed_paths and not request.user.is_authenticated:
            return redirect('/')

        return self.get_response(request)

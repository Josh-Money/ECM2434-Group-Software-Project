from django.shortcuts import redirect

class RedirectLoggedOutUsersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allowed paths for unauthenticated users
        logged_out_allowed_paths = ['/', '/sign-up/', '/privacy-policy', '/privacy-policy/']
        logged_in_disallowed_paths = ['/', '/sign-up', '/sign-up/']


        # If user is not authenticated and trying to access a restricted page, redirect them
        if request.path not in logged_out_allowed_paths and not request.user.is_authenticated:
            print('AAAAAAAAAAAA', request.path)
            return redirect('/')  # Redirect to login instead of home
        elif request.path in logged_in_disallowed_paths and request.user.is_authenticated:
            return redirect('/home/')

        return self.get_response(request)


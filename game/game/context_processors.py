def global_context(request):
    return {
        "is_authenticated": request.user.is_authenticated,
        "user": request.user,
    }

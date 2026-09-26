from django.contrib.auth import logout


class SingleSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            session_key = request.session.session_key or ""
            if not session_key or request.user.active_session_key != session_key:
                logout(request)
        return self.get_response(request)

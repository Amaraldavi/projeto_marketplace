from django.conf import settings
from django.shortcuts import redirect


class LegacyFrontendRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if self.should_redirect(request.path_info):
            return self.redirect_to_frontend(request)
        return self.get_response(request)

    def should_redirect(self, path):
        excluded_prefixes = (
            '/api/',
            '/admin/',
            '/accounts/',
            '/static/',
            '/media/',
            '/webhooks/mercadopago/',
        )

        if any(path.startswith(prefix) for prefix in excluded_prefixes):
            return False

        return True

    def redirect_to_frontend(self, request):
        frontend_base = getattr(settings, 'FRONTEND_URL', 'http://localhost:8080').rstrip('/')
        return redirect(f"{frontend_base}{request.get_full_path()}")

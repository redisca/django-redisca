from django.shortcuts import redirect as redirect_response
from .models import Redirect


class RedirectMiddleware:
    def process_response(self, request, response):
        if response.status_code != 404:
            return response

        request_path = request.get_full_path()
        if request_path.endswith('/'):
            request_path = request_path[:-1]

        try:
            redirect = Redirect.objects.get(old_path=request_path, regex=False)
            return redirect_response(redirect.new_path, permanent=redirect.permanent)
        except Redirect.DoesNotExist:
            for redirect in Redirect.objects.filter(regex=True):
                new_path = redirect.resolve(request_path)
                if new_path:
                    return redirect_response(new_path, permanent=redirect.permanent)

        return response

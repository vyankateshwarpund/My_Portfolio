from .models import Visitor

class VisitorAnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Log visitor for non-static and non-admin requests
        path = request.path
        if not (path.startswith('/static/') or path.startswith('/media/') or path.startswith('/admin/') or path.startswith('/favicon.ico')):
            try:
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0].strip()
                else:
                    ip = request.META.get('REMOTE_ADDR')

                user_agent = request.META.get('HTTP_USER_AGENT', '')
                referrer = request.META.get('HTTP_REFERER', '')

                Visitor.objects.create(
                    ip_address=ip,
                    user_agent=user_agent[:500] if user_agent else '',
                    page_url=path[:500],
                    referrer=referrer[:500] if referrer else ''
                )
            except Exception:
                pass # Fail silently so middleware doesn't interrupt request

        return response

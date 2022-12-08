from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class LastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def last_activity(self, request):
        user = User.objects.filter(username=request.user)
        user.update(last_activity=timezone.now())

    def __call__(self, request):
        response = self.get_response(request)
        self.last_activity(request)
        return response
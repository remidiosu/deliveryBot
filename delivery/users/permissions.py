from django.conf import settings
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import View


class BotSharedSecretPermission(BasePermission):
    def has_permission(self, request: Request, view: View):
        header = request.headers.get("X-Bot-Secret")
        return bool(header and header == getattr(settings, "BOT_SHARED_SECRET", None))

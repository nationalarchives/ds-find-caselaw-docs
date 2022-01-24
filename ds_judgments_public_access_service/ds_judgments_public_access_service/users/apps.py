from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "ds_judgments_public_access_service.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import ds_judgments_public_access_service.users.signals  # noqa F401
        except ImportError:
            pass

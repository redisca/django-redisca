from django.conf import settings

ADMIN_SIDEBAR_ITEMS = getattr(settings, 'ADMIN_SIDEBAR_ITEMS', ())

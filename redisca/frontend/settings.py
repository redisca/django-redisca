import os
from django.conf import settings


FRONTEND_DIRS = getattr(settings, 'FRONTEND_DIRS', {
    'svg': os.path.join(settings.BASE_DIR, 'frontend', 'svg'),
})

FRONTEND_BUILDER = {
    'COMMAND': 'gulp',
    'ARGS': '',
    'WATCH_TASK': 'watch',
    'BUILD_TAKS': 'default',
}

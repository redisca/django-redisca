import subprocess
import tempfile
import atexit
import os

from django.contrib.staticfiles.management.commands.runserver \
    import Command as BaseRunserverCommand

from redisca.frontend import settings
from ..utils import ExitHook
exit_hook = ExitHook()


LOCKFILE = os.path.join(
    tempfile.gettempdir(), 'django-frontend.lock')

BUILDER, BUILDER_ARGS, WATCH_TASK, BUILD_TAKS = map(
    settings.FRONTEND_BUILDER.get,
    ('COMMAND', 'ARGS', 'WATCH_TASK', 'BUILD_TAKS'),
)


class Command(BaseRunserverCommand):
    arguments = {
        '--frontend': dict(dest='frontend', action='store_true', help='Run with frontend server.'),
    }

    def add_arguments(self, parser):
        for flag, args in self.arguments.items():
            parser.add_argument(flag, **args)
        super().add_arguments(parser)

    def inner_run(self, *args, **options):
        atexit.register(self.unlock_pid)

        if options['frontend'] and not self.is_running():
            self.run_builder()
            self.lock_pid()

        super().inner_run(*args, **options)

    def lock_pid(self):
        open(LOCKFILE, 'a').close()

    def unlock_pid(self):
        if exit_hook.code is None:
            if self.is_running():
                self.stdout.write('Stopping "{}"...'.format(BUILDER))
                os.remove(LOCKFILE)

    def is_running(self):
        return os.path.isfile(LOCKFILE)

    def run_builder(self):
        proc_args = dict(shell=True, stdin=subprocess.PIPE,
                         stdout=self.stdout, stderr=self.stderr)
        tasks = []
        tasks.append(BUILD_TAKS)
        tasks.append(WATCH_TASK)

        command = ' '.join([BUILDER, ' '.join(tasks), BUILDER_ARGS]).strip()
        self.stdout.write('Starting "{}"...'.format(command))
        subprocess.Popen(command, **proc_args)

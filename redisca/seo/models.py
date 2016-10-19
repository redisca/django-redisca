from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
import re


class Redirect(models.Model):
    old_path = models.CharField(max_length=255, db_index=True)
    new_path = models.CharField(max_length=255, blank=True)
    regex = models.BooleanField(default=False)
    permanent = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)

    class Meta:
        unique_together = ('old_path', 'new_path')
        ordering = ('-priority',)

    def __str__(self):
        return self.old_path

    def resolve(self, url):
        if self.regex:
            match = re.search(self.old_path, url, re.I)
            if not match:
                return None
            new_path = self.new_path
            for i, group in enumerate(match.groups(), 1):
                new_path = new_path.replace('$' + str(i), group)
            return new_path
        return self.new_path


@receiver(pre_save, sender=Redirect)
def remove_trailing_slash(sender, instance, **kwargs):
    if instance.old_path.endswith('/'):
        instance.old_path = instance.old_path[:-1]

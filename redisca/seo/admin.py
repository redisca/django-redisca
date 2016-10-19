from django.contrib import admin
from .models import Redirect


@admin.register(Redirect)
class RedirectAdmin(admin.ModelAdmin):
    list_display = ('old_path', 'new_path', 'permanent')
    search_fields = ('old_path', 'new_path')

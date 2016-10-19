from django.contrib.admin.sites import site
from django.template import Library

from .. import settings

register = Library()


@register.inclusion_tag('admin_sidebar/admin_sidebar.html', takes_context=True)
def admin_sidebar(context):
    if settings.ADMIN_SIDEBAR_ITEMS:
        items = settings.ADMIN_SIDEBAR_ITEMS
    else:
        request = context['request']
        items = get_apps_items(request)

    return {'items': items}


def get_apps_items(request):
    app_list = []
    for app in site.get_app_list(request):
        model_list = []
        for model in app['models']:
            model_list.append((model['name'], model['admin_url']))

        app_name = app['name']
        if app['app_label'] == 'auth':
            app_name = 'Authentication'

        app_list.append((app_name, app['app_url'], model_list))
    return app_list

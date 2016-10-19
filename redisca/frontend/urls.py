from django.conf.urls import url
from redisca.frontend import views


app_name = 'frontend'

urlpatterns = [
    url(r'^$', views.template_list, name='template_list'),
    url(r'^([a-zA-Z0-9_\./\-]+)$', views.static_template, name='template'),
]

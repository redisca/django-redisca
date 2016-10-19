from django.template import loader, TemplateDoesNotExist
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.conf import settings
import os

TEMPLATES_DIR = os.path.join(settings.BASE_DIR, 'templates')


def template_list(request):
    tree = os.walk(TEMPLATES_DIR)
    ignore_dirs = ['layouts']
    file_list = []

    for (dirpath, dirnames, filenames) in tree:
        for filename in filenames:
            filename, _ = os.path.splitext(filename)
            relpath = os.path.relpath(dirpath, TEMPLATES_DIR)
            template_name = ((relpath + '/') if relpath != '.' else '') + filename

            ignored = False
            for ignore_dir in ignore_dirs:
                if template_name.startswith(ignore_dir):
                    ignored = True
                    break

            if not ignored:
                file_list.append(template_name)

    return render(request, 'frontend/template_list.html', {'templates': file_list})


def static_template(request, template_name='index'):
    try:
        template = loader.select_template([
            template_name + '.html',
            template_name + '/index.html',
        ])
    except TemplateDoesNotExist:
        raise Http404('Template %s does not exist' % template_name)

    return HttpResponse(template.render())

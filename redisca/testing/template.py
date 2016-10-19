from django.template import Template, Context
from unittest import TestCase


class TemplateTestCase(TestCase):
    library = None

    def render(self, content, **context_data):
        load_tpl = ''
        if self.library:
            load_tpl = '{% load ' + self.library + ' %}'

        tpl = Template(load_tpl + content)
        context = Context(context_data)
        return tpl.render(context)


def render_template(content='', context_data={}):
    tpl = Template(content)
    context = Context(context_data)
    result = tpl.render(context)
    return result

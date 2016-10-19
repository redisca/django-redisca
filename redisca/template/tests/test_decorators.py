from nose import tools as test
from redisca.testing.template import render_template
from ..decorators import template_func


def test_template_func():
    undecorated = lambda *args: sum(args)
    decorated = template_func(undecorated)
    assert decorated(1, 2, 3) == undecorated(1, 2, 3)
    result = render_template('{{ decorated|safe }}', {'decorated': decorated})
    assert result.startswith('<function test_template_func.<locals>.<lambda>')

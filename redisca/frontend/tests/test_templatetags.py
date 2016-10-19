import os
from nose import tools as test
from django.test import override_settings

from redisca.frontend.templatetags.frontend import (
    svg_icon, optimize_svg, wrap_comment)


def test_optimize_svg():
    svg = """
    <svg id="1" attra="1" attrb="2">
        <g>
            <circle>
        </g>
    </svg>
    """
    test.assert_equal(optimize_svg(svg), '<svg attra="1" attrb="2"><g><circle></g></svg>')
    test.assert_equal(optimize_svg('not a svg'), 'not a svg')


def test_wrap_comment():
    result = wrap_comment('icon.svg', '<svg></svg>')
    expect = '<!-- icon.svg --><svg></svg><!-- /icon.svg -->'
    test.assert_equal(result, expect)


@override_settings(FRONTEND_DIRS={
    'svg': os.path.join(os.path.dirname(__file__), 'fixtures'),
})
def test_svg_icon():
    expect = '<!-- icon.svg --><svg><g></g></svg><!-- /icon.svg -->'
    test.assert_equal(svg_icon('icon.svg'), expect)
    test.assert_equal(svg_icon('icon.svg'), expect)  # second call for cache test

    expect = '<!-- ERROR: svg icon not found in redisca/frontend/tests/fixtures/not.svg -->'
    test.assert_equal(svg_icon('not.svg'), expect)

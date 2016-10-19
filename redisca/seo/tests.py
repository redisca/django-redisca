from nose import tools as test
from django.test import RequestFactory
from django.http import HttpResponse, HttpResponseNotFound
from .models import Redirect, remove_trailing_slash
from .middleware import RedirectMiddleware


class TestRedirect:
    def test_str(self):
        redirect = Redirect(old_path='/news')
        test.assert_equal(str(redirect), '/news')

    def test_resolve(self):
        redirect = Redirect(old_path='/news', new_path='/')
        test.assert_equal(redirect.resolve('/news'), '/')
        test.assert_equal(redirect.resolve('/blog'), '/')

        redirect_regex = Redirect(old_path='^/news/(.*)$', new_path='/blog/$1', regex=True)
        test.assert_equal(redirect_regex.resolve('/news/'), '/blog/')
        test.assert_equal(redirect_regex.resolve('/news/1'), '/blog/1')
        test.assert_is_none(redirect_regex.resolve('/blog'))

    def test_remove_trailing_slash(self):
        redirect = Redirect(old_path='/news/')
        remove_trailing_slash(Redirect, redirect)
        test.assert_equal(redirect.old_path, '/news')


class TestRedirectMiddleware:
    def setup(self):
        self.middleware = RedirectMiddleware()
        self.factory = RequestFactory()

    def request(self, url, response=HttpResponseNotFound()):
        request = self.factory.get(url)
        return self.middleware.process_response(request, response)

    def assert_redirects(self, response, target_url, permanent):
        status_code = 301 if permanent else 302
        test.assert_equal(response.status_code, status_code)
        test.assert_equal(response.url, target_url)

    def test_process_response_basic(self):
        redirect = Redirect.objects.create(old_path='/news', new_path='/blog')
        response = self.request('/news/')
        self.assert_redirects(response, '/blog', permanent=False)
        redirect.delete()

    def test_process_response_permanent(self):
        redirect = Redirect.objects.create(
            old_path='/news',
            new_path='/blog',
            permanent=True,
        )
        response = self.request('/news/')
        self.assert_redirects(response, '/blog', permanent=True)
        redirect.delete()

    def test_process_response_regex(self):
        redirect = Redirect.objects.create(
            old_path='^/news/(.*)$',
            new_path='/blog/$1',
            permanent=True,
            regex=True,
        )
        response = self.request('/news/1')
        self.assert_redirects(response, '/blog/1', permanent=True)
        redirect.delete()

    def test_process_response_non_404(self):
        response = HttpResponse()
        middleware_response = self.request('/news', response=response)
        test.assert_equal(response, middleware_response)

    def test_process_response_non_redirect(self):
        response = HttpResponseNotFound()
        middleware_response = self.request('/news', response=response)
        test.assert_equal(response, middleware_response)

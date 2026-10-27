from django.http import HttpRequest
from django.test import TestCase
from lists.views import home_page

class HomePageTest(TestCase):
        def test_home_page_returns_html(self):
            request = HttpRequest()
            response = home_page(request)
            html = response.content.decoder('utf-8')
            self.assertIn(member: "<title>To-Do</title>", html)
            self.assertTrue(html.startswith("<html>"))
# Create your tests here.

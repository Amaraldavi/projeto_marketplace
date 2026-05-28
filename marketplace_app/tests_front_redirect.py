from django.test import TestCase, Client


class FrontRedirectTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_root_redirects_to_frontend(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'http://localhost:8080/')

    def test_login_redirects_to_frontend_login_route(self):
        response = self.client.get('/login/')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'http://localhost:8080/login/')

    def test_api_routes_are_not_redirected(self):
        response = self.client.get('/api/listings/')

        self.assertEqual(response.status_code, 200)

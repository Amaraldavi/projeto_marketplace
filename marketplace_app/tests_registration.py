from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import CommonProfile, StoreProfile


class RegistrationIntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('api_register')

    def test_individual_registration_creates_user_and_profile(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'ComplexPwd123!',
            'is_store': False,
            'cpf': '529.982.247-25',
            'birth_date': '1990-01-01',
            'phone': '(11) 99999-9999',
            'cep': '00000-000',
            'address': 'Rua Test, 123',
        }

        response = self.client.post(self.register_url, data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        User = get_user_model()
        user = User.objects.filter(username='testuser').first()
        self.assertIsNotNone(user)
        profile = CommonProfile.objects.filter(user=user).first()
        self.assertIsNotNone(profile)

    def test_store_registration_creates_user_and_store_profile(self):
        data = {
            'username': 'storeuser',
            'email': 'store@example.com',
            'password': 'AnotherPwd123!',
            'is_store': True,
            'cnpj': '04.252.011/0001-10',
            'razao_social': 'ACME Ltda',
            'fantasy_name': 'ACME',
            'state_registration': '12345',
            'responsible_name': 'Owner',
            'responsible_cpf': '529.982.247-25',
            'store_phone': '(11) 98888-8888',
            'store_email': 'store@example.com',
            'commercial_cep': '00000-000',
            'commercial_address': 'Rua Loja, 10',
        }

        response = self.client.post(self.register_url, data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        User = get_user_model()
        user = User.objects.filter(username='storeuser').first()
        self.assertIsNotNone(user)
        self.assertTrue(user.is_store)
        profile = StoreProfile.objects.filter(user=user).first()
        self.assertIsNotNone(profile)

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketplace.settings')
import django
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from marketplace_app.models import CommonProfile

client = Client()
payload = {
    'username': 'repro_user',
    'email': 'repro@example.com',
    'password': 'ComplexPwd123!',
    'is_store': False,
    'cpf': '529.982.247-25',
    'birth_date': '1990-01-01',
    'phone': '11999999999',
    'cep': '01001000',
    'address': 'Rua X',
}
response = client.post('/api/register/', payload, content_type='application/json')
print('status', response.status_code)
print('body', response.content.decode())
User = get_user_model()
print('user_exists', User.objects.filter(username='repro_user').exists())
print('profile_exists', CommonProfile.objects.filter(user__username='repro_user').exists())

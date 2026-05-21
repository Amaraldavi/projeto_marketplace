import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketplace.settings')
django.setup()
from django.template.loader import render_to_string

class DummyImage:
    def __init__(self, url):
        self.image = type('I', (), {'url': url})

class DummyListing:
    def __init__(self, id):
        self.id = id
        self.title = 'Test'
        self.description = 'Desc'
        self.price = 10
        self.category = type('C', (), {'name': 'Teste'})
        self.seller = type('S', (), {'username': 'seller'})
        self.is_featured = False
        self.is_store_featured = False
        self.status = 'active'
        self._images = [DummyImage('/static/img.png')]

    @property
    def get_condition_display(self):
        return 'Novo'

    def images(self):
        return self

    def all(self):
        return self._images

    @property
    def first(self):
        return self._images[0]

context = {
    'carousel_products': [],
    'featured_products': [DummyListing(1)],
    'anuncios': [DummyListing(2)],
    'categories': [],
    'selected_category': None,
    'user': type('U', (), {'is_authenticated': True, 'username': 'test'})
}
html = render_to_string('home.html', context)
print('listing_detail' in html)
print('add_to_cart' in html)
print('btn-details count', html.count('btn-details'))
print('btn-buy count', html.count('btn-buy'))

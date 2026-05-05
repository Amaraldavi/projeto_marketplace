# Generated migration to update categories

from django.db import migrations


def create_categories(apps, schema_editor):
    Category = apps.get_model('marketplace_app', 'Category')
    
    # Remove Eletrônicos if it exists
    Category.objects.filter(name='Eletrônicos').delete()
    
    # Create new categories
    categories = [
        'Dispositivos pessoais',
        'Informática',
        'Games',
        'TV e audio',
        'Foto e video',
        'Todos'
    ]
    
    for category_name in categories:
        Category.objects.get_or_create(name=category_name)


def reverse_categories(apps, schema_editor):
    Category = apps.get_model('marketplace_app', 'Category')
    Category.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace_app', '0002_listing_is_featured_listing_is_store_featured'),
    ]

    operations = [
        migrations.RunPython(create_categories, reverse_categories),
    ]

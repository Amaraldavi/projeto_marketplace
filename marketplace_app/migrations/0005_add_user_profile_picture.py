from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace_app', '0004_add_comment_and_cart_models'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures/'),
        ),
    ]

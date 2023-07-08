# Generated by Django 4.1 on 2023-06-15 20:39

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('plan', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userplan',
            unique_together={('user', 'plan', 'is_active')},
        ),
    ]

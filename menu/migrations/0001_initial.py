# Generated by Django 4.1 on 2023-05-22 21:57

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('theme', '0002_alter_theme_background_image_alter_theme_preview'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('image', models.CharField(max_length=255)),
                ('number_of_qrcodes', models.IntegerField(default=1)),
                ('code', models.PositiveIntegerField(default=81413, unique=True)),
                ('telephone', models.CharField(blank=True, max_length=25, null=True)),
                ('phone', models.CharField(blank=True, max_length=25, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_paid', models.BooleanField(default=False)),
                ('last_time_paid', models.DateTimeField(default=datetime.datetime(2023, 5, 22, 21, 57, 53, 846758))),
                ('primary_color', models.CharField(default='#007bff', max_length=7)),
                ('secondary_color', models.CharField(default='#6c757d', max_length=7)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('theme', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='theme.theme')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

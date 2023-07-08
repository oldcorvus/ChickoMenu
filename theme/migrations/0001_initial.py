# Generated by Django 4.1 on 2023-05-21 22:13

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('preview', models.ImageField(upload_to='theme_preview')),
                ('background_image', models.ImageField(upload_to='theme_image')),
                ('font_family', models.CharField(default='Arial, sans-serif', max_length=255)),
                ('menu_background_color', models.CharField(default='#f8f9fa', max_length=7)),
                ('menu_text_color', models.CharField(default='#343a40', max_length=7)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

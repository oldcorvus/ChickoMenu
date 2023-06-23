# Generated by Django 4.1 on 2023-06-23 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theme', '0004_rename_background_image_theme_header_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='theme',
            name='font_family',
            field=models.CharField(default='Vazir', max_length=255),
        ),
        migrations.AlterField(
            model_name='theme',
            name='header_color',
            field=models.CharField(default='#2196f3', max_length=7),
        ),
        migrations.AlterField(
            model_name='theme',
            name='menu_background_color',
            field=models.CharField(default='#fff', max_length=7),
        ),
        migrations.AlterField(
            model_name='theme',
            name='menu_text_color',
            field=models.CharField(default='#000', max_length=7),
        ),
    ]
# Generated by Django 4.1 on 2023-07-09 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theme', '0006_theme_menu_item_background_color_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='theme',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
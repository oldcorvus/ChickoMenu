# Generated by Django 4.1 on 2023-06-23 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0008_alter_menuitem_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='image',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

# Generated by Django 4.1 on 2023-07-09 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0009_alter_menu_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='menu',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
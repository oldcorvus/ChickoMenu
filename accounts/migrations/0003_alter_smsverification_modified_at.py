# Generated by Django 4.1 on 2023-07-09 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_plans'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smsverification',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]

# Generated by Django 4.1 on 2023-05-21 18:02

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SMSVerification',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('security_code', models.CharField(max_length=120)),
                ('phone_number', models.CharField(max_length=11)),
                ('session_token', models.CharField(max_length=500)),
                ('is_verified', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'SMS Verification',
                'verbose_name_plural': 'SMS Verifications',
                'db_table': 'sms_verification',
                'ordering': ('-modified_at',),
                'unique_together': {('security_code', 'phone_number', 'session_token')},
            },
        ),
    ]

# Generated by Django 5.1.1 on 2024-11-27 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='verification_status',
            field=models.CharField(choices=[('verified', 'Verified'), ('not_verified', 'Not Verified')], default='not_verified', max_length=20),
        ),
    ]
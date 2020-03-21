# Generated by Django 3.0.4 on 2020-03-11 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0002_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='bio',
        ),
        migrations.AddField(
            model_name='profile',
            name='signup_confirmation',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 3.0.4 on 2020-03-20 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0011_auto_20200315_1310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='email',
            field=models.EmailField(max_length=150, unique=True),
        ),
    ]

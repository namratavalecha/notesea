# Generated by Django 3.0.4 on 2020-03-14 09:52

from django.db import migrations, models
import notes.models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0003_auto_20200311_1834'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='image',
            field=models.ImageField(default=1, upload_to=notes.models.get_image_filename),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Images',
        ),
    ]

# Generated by Django 5.0.1 on 2024-01-12 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0006_photo_path'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='path',
        ),
        migrations.AlterField(
            model_name='photo',
            name='files',
            field=models.ImageField(upload_to='file_uploads/'),
        ),
    ]

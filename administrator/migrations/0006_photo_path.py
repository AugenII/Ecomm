# Generated by Django 5.0.1 on 2024-01-12 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0005_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='path',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]

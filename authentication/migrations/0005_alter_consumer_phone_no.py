# Generated by Django 5.0.1 on 2024-01-17 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_remove_consumer_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consumer',
            name='phone_no',
            field=models.CharField(max_length=15),
        ),
    ]

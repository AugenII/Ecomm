# Generated by Django 5.0.1 on 2024-01-25 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0023_alter_order_total_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='quantity',
            field=models.IntegerField(null=True),
        ),
    ]

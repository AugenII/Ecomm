# Generated by Django 5.0.1 on 2024-01-12 10:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0012_payment'),
        ('authentication', '0004_remove_consumer_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=50)),
                ('delivery_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrator.address')),
                ('payment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='administrator.payment')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrator.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.consumer')),
            ],
        ),
    ]

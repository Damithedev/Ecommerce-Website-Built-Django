# Generated by Django 4.2.9 on 2024-01-15 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_product_cashondelivery'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]

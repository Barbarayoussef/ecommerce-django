# Generated by Django 5.0.12 on 2025-07-04 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_profile_old_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='expiry_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='is_expirable',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='is_shippable',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='weight',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
    ]

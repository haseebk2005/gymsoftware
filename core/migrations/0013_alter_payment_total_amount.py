# Generated by Django 5.0.7 on 2024-11-11 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_payment_overpayment_alter_gymmember_activation_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='total_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
    ]

# Generated by Django 5.0.7 on 2024-11-13 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_alter_payment_total_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='gymmember',
            name='last_fee_reset_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
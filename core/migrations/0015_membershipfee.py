# Generated by Django 5.0.7 on 2024-11-13 11:02

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_gymmember_last_fee_reset_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='MembershipFee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('single time', 'single time'), ('single time with electric machine', 'single time with electric machine'), ('double time', 'double time'), ('double time with electric machine', 'double time with electric machine')], max_length=50, unique=True)),
                ('fee', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=8)),
            ],
        ),
    ]

# Generated by Django 5.0.7 on 2024-11-06 07:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GymMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=10)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pics/')),
                ('membership_id', models.CharField(max_length=20, unique=True)),
                ('membership_type', models.CharField(choices=[('single time', 'single time'), ('single time with electric machine', 'single time with electric machine'), ('double time', 'double time'), ('double time with electric machine', 'double time with electric machine')], max_length=50)),
                ('active_status', models.BooleanField(default=True)),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('height', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('bmi', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('fitness_goal', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('emergency_contact_relation', models.CharField(blank=True, max_length=50, null=True)),
                ('joined_date', models.DateField(auto_now_add=True)),
                ('last_visit_date', models.DateField(blank=True, null=True)),
                ('additional_notes', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in_time', models.DateTimeField(auto_now_add=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.gymmember')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_date', models.DateField(auto_now_add=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('remaining_balance', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.gymmember')),
            ],
        ),
    ]

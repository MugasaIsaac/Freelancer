# Generated by Django 3.0.3 on 2020-02-25 08:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(max_length=25)),
                ('last_name', models.CharField(max_length=25)),
                ('user_name', models.CharField(max_length=25)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=16, unique=True, validators=[django.core.validators.RegexValidator(message='Phone number must be in international format: `+256123456789`.', regex='^\\+?1?\\d{10,13}$')])),
                ('role', models.CharField(choices=[('FA', 'FREELANCER ADMIN'), ('CA', 'COMPANY ADMIN'), ('NU', 'NORMAL USER')], default='NU', max_length=2, verbose_name='user role')),
                ('is_verified', models.BooleanField(default=False)),
                ('is_company', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

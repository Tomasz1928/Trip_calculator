# Generated by Django 5.0.7 on 2024-07-18 18:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('tabel_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('start', models.CharField(max_length=255)),
                ('end', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=255)),
                ('firstname', models.CharField(blank=True, max_length=255, null=True)),
                ('lastname', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cost',
            fields=[
                ('cost_id', models.AutoField(primary_key=True, serialize=False)),
                ('cost_name', models.CharField(max_length=255)),
                ('value', models.IntegerField()),
                ('trip_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trip_calculator.trip')),
                ('payer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trip_calculator.user')),
            ],
        ),
        migrations.CreateModel(
            name='Splited',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trip_calculator.cost')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trip_calculator.user')),
            ],
        ),
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('active', models.BooleanField(default=False)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trip_calculator.user')),
            ],
        ),
        migrations.CreateModel(
            name='UserTrip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trip_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trip_calculator.trip')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trip_calculator.user')),
            ],
        ),
    ]

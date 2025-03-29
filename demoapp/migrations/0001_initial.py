# Generated by Django 3.1.13 on 2025-03-27 10:44

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=100)),
                ('customer_phone', models.CharField(max_length=15)),
                ('purchase_date', models.DateTimeField(auto_now_add=True)),
                ('Sub_total', models.FloatField(default=0.0)),
                ('GST', models.FloatField(default=0.0)),
                ('Total', models.FloatField(default=0.0)),
                ('items', models.JSONField(default=list)),
            ],
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='images/')),
                ('description', models.TextField()),
                ('author', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100)),
                ('initial_stock', models.FloatField(default=0.0)),
                ('current_stock', models.FloatField(default=0.0)),
                ('total_sold', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=100)),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='demoapp.stock')),
            ],
        ),
    ]

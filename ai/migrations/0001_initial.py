# Generated by Django 5.1.5 on 2025-03-25 15:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=4000)),
                ('type', models.CharField(choices=[('HT', 'HEALTH'), ('NT', 'NUTRITION'), ('AT', 'ACTIVITY')], max_length=12)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_in', models.DateTimeField()),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pets.pet')),
            ],
        ),
    ]

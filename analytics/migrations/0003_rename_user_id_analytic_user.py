# Generated by Django 5.1.5 on 2025-05-06 13:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0002_rename_analytics_analytic'),
    ]

    operations = [
        migrations.RenameField(
            model_name='analytic',
            old_name='user_id',
            new_name='user',
        ),
    ]

# Generated by Django 5.1.5 on 2025-03-10 19:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0002_pet_race'),
    ]

    operations = [
        migrations.RenameField(
            model_name='petrace',
            old_name='race',
            new_name='name',
        ),
    ]

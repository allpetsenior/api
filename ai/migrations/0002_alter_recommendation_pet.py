# Generated by Django 5.1.5 on 2025-04-10 00:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai', '0001_initial'),
        ('pets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recommendation',
            name='pet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pets.pet'),
        ),
    ]

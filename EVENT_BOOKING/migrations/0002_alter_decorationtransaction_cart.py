# Generated by Django 5.1 on 2025-03-15 10:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EVENT_BOOKING', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='decorationtransaction',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EVENT_BOOKING.event'),
        ),
    ]

# Generated by Django 4.0.3 on 2022-04-12 15:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0044_alter_appointmentadminmodel_timeduration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointmentadminmodel',
            name='timeDuration',
        ),
    ]

# Generated by Django 4.0.3 on 2022-04-09 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0037_appointmentmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointmentmodel',
            name='email',
            field=models.EmailField(blank=True, max_length=250, null=True),
        ),
    ]
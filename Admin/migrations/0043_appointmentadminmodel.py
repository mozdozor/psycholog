# Generated by Django 4.0.3 on 2022-04-12 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0042_rename_name_appointmentmodel_fullname_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='appointmentAdminModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, max_length=250, null=True)),
                ('starting_time', models.TimeField(blank=True, max_length=250, null=True)),
                ('finishing_time', models.TimeField(blank=True, max_length=250, null=True)),
                ('timeDuration', models.TextField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'verbose_name': 'RandevuAdmin',
                'verbose_name_plural': 'RandevularAdmin',
                'db_table': 'appointmentAdmin',
            },
        ),
    ]
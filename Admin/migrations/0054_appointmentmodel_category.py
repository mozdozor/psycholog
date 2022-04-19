# Generated by Django 4.0.3 on 2022-04-16 05:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0053_appointmentcategorymodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointmentmodel',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modelssOfCategory', to='Admin.appointmentcategorymodel'),
        ),
    ]
# Generated by Django 4.0.3 on 2022-04-13 06:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0046_appointmentmodel_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificationmodel',
            name='appointmentObject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notificationsOfAppo', to='Admin.appointmentmodel'),
        ),
    ]

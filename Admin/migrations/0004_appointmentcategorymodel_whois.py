# Generated by Django 4.0.3 on 2022-06-28 16:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Admin', '0003_appointmentadminmodel_whois'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointmentcategorymodel',
            name='whois',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relatedAppointmentCategoryModels', to=settings.AUTH_USER_MODEL),
        ),
    ]

# Generated by Django 4.0.3 on 2022-04-01 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0030_socialmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialmodel',
            name='facebook',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='socialmodel',
            name='instagram',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='socialmodel',
            name='pinterest',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
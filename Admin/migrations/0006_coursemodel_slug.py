# Generated by Django 4.0.3 on 2022-03-18 07:00

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0005_pagemodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursemodel',
            name='slug',
            field=autoslug.fields.AutoSlugField(blank=True, editable=False, null=True, populate_from='title', unique=True),
        ),
    ]

# Generated by Django 4.0.3 on 2022-03-15 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0003_alter_coursemodel_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursemodel',
            name='image',
            field=models.ImageField(upload_to='courseImages'),
        ),
    ]

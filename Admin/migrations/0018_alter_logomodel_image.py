# Generated by Django 4.0.3 on 2022-03-28 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0017_logomodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logomodel',
            name='image',
            field=models.ImageField(default='logo/logo.png', upload_to='logoImages'),
        ),
    ]
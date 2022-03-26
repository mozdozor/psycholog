# Generated by Django 4.0.3 on 2022-03-26 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psikolog', '0008_alter_customusermodel_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingcoursemodel',
            name='average_star',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='billingcoursemodel',
            name='meta_description',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='billingcoursemodel',
            name='meta_keywords',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='billingcoursemodel',
            name='meta_title',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='billingcoursemodel',
            name='none_average_star',
            field=models.PositiveSmallIntegerField(blank=True, default=5, null=True),
        ),
    ]

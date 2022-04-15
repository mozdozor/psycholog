# Generated by Django 4.0.3 on 2022-04-13 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0051_remove_pagemodel_view_name_topmenumodel_page_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topmenumodel',
            name='page',
        ),
        migrations.AddField(
            model_name='bottommenumodel',
            name='meta_description',
            field=models.CharField(blank=True, max_length=170, null=True),
        ),
        migrations.AddField(
            model_name='bottommenumodel',
            name='meta_keywords',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='bottommenumodel',
            name='meta_title',
            field=models.CharField(blank=True, max_length=65, null=True),
        ),
        migrations.AddField(
            model_name='topmenumodel',
            name='meta_description',
            field=models.CharField(blank=True, max_length=170, null=True),
        ),
        migrations.AddField(
            model_name='topmenumodel',
            name='meta_keywords',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='topmenumodel',
            name='meta_title',
            field=models.CharField(blank=True, max_length=65, null=True),
        ),
        migrations.AlterField(
            model_name='pagemodel',
            name='meta_description',
            field=models.CharField(blank=True, max_length=170, null=True),
        ),
        migrations.AlterField(
            model_name='pagemodel',
            name='meta_keywords',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='pagemodel',
            name='meta_title',
            field=models.CharField(blank=True, max_length=65, null=True),
        ),
    ]
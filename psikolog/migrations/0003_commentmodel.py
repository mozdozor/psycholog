# Generated by Django 4.0.3 on 2022-03-17 07:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0004_alter_coursemodel_image'),
        ('psikolog', '0002_alter_customusermodel_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_recommend', models.BooleanField(default=False)),
                ('star', models.PositiveSmallIntegerField(blank=True, default=0, null=True)),
                ('none_star', models.PositiveSmallIntegerField(blank=True, default=5, null=True)),
                ('comment', models.TextField(blank=True, default='', null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_published', models.BooleanField(default=False)),
                ('comment_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='his_comments', to=settings.AUTH_USER_MODEL)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='all_comments', to='Admin.coursemodel')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='psikolog.commentmodel')),
            ],
            options={
                'verbose_name': 'Yorum',
                'verbose_name_plural': 'Yorumlar',
                'db_table': 'comment',
                'ordering': ('-created_date',),
            },
        ),
    ]

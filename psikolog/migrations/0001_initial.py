# Generated by Django 4.0.3 on 2022-05-20 15:59

import autoslug.fields
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('Admin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUserModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='get_full_name', unique=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('email', models.EmailField(max_length=250, unique=True)),
                ('phone_number', models.CharField(max_length=250)),
                ('image', models.ImageField(default='avatar/no-avatar.png', upload_to='profile_images')),
                ('about', models.TextField(blank=True, default='', null=True)),
                ('city', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('state', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('country', models.CharField(blank=True, default='Türkiye', max_length=50, null=True)),
                ('address', models.CharField(blank=True, default='', max_length=450, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Kullanıcı',
                'verbose_name_plural': 'Kullanıcılar',
                'db_table': 'customUser',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='mediaGalleryImageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='mediaGalleryImages')),
                ('image2', models.ImageField(blank=True, null=True, upload_to='mediaGalleryImages')),
                ('title', models.CharField(max_length=300)),
                ('sira', models.PositiveSmallIntegerField(blank=True, default=0, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_date', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name': 'MediaGalleryImage',
                'verbose_name_plural': 'MediaGalleryImages',
                'db_table': 'MediaGalleryImages',
            },
        ),
        migrations.CreateModel(
            name='mediaGalleryVideoModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=300)),
                ('image', models.ImageField(upload_to='mediaGalleryVideoImages')),
                ('title', models.CharField(max_length=300)),
                ('sira', models.PositiveSmallIntegerField(blank=True, default=0, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_date', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name': 'MediaGalleryVideo',
                'verbose_name_plural': 'MediaGalleryVideos',
                'db_table': 'MediaGalleryVideos',
            },
        ),
        migrations.CreateModel(
            name='sliderModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='sliderImages')),
                ('top_title', models.CharField(max_length=300)),
                ('bottom_title', models.CharField(max_length=300)),
                ('url', models.CharField(blank=True, max_length=300, null=True)),
                ('sira', models.PositiveSmallIntegerField(blank=True, default=0, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_date', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name': 'Slider',
                'verbose_name_plural': 'Sliderlar',
                'db_table': 'Slider',
            },
        ),
        migrations.CreateModel(
            name='orderModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveSmallIntegerField(blank=True, default=0, null=True)),
                ('status', models.CharField(max_length=10)),
                ('merchant_oid', models.CharField(max_length=250)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_date', models.DateTimeField(auto_now=True, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin.coursemodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderCourses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Siparis',
                'verbose_name_plural': 'Siparisler',
                'db_table': 'siparis',
            },
        ),
        migrations.CreateModel(
            name='hasWatchedModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_date', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watchedVideos', to=settings.AUTH_USER_MODEL)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin.coursesessionvideomodel')),
            ],
            options={
                'verbose_name': 'İzlenen Video',
                'verbose_name_plural': 'İzlenen Videolar',
                'db_table': 'watchedVideos',
            },
        ),
        migrations.CreateModel(
            name='favouriteCourseModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin.coursemodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favouriteCourses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Favori Kurs',
                'verbose_name_plural': 'Favori Kurslar',
                'db_table': 'Favori_Kurslar',
            },
        ),
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
                ('blog', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='blog_comments', to='Admin.blogmodel')),
                ('comment_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='his_comments', to=settings.AUTH_USER_MODEL)),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='all_comments', to='Admin.coursemodel')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='psikolog.commentmodel')),
            ],
            options={
                'verbose_name': 'Yorum',
                'verbose_name_plural': 'Yorumlar',
                'db_table': 'comment',
                'ordering': ('-created_date',),
            },
        ),
        migrations.CreateModel(
            name='billingCourseModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='billingCourseImage')),
                ('title', models.CharField(max_length=300)),
                ('slug', autoslug.fields.AutoSlugField(blank=True, editable=False, null=True, populate_from='title', unique=True)),
                ('description', models.TextField()),
                ('bottomDescription', models.TextField()),
                ('videoCount', models.PositiveSmallIntegerField(default=0)),
                ('average_star', models.PositiveSmallIntegerField(blank=True, default=0, null=True)),
                ('none_average_star', models.PositiveSmallIntegerField(blank=True, default=5, null=True)),
                ('price', models.PositiveSmallIntegerField(default=0)),
                ('meta_title', models.CharField(blank=True, max_length=500, null=True)),
                ('meta_description', models.CharField(blank=True, max_length=500, null=True)),
                ('meta_keywords', models.CharField(blank=True, max_length=500, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_date', models.DateTimeField(auto_now=True, null=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='userBillingCourses', to=settings.AUTH_USER_MODEL)),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='billingCourses', to='Admin.coursemodel')),
                ('payment_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paymentAllCourse', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Fatura',
                'verbose_name_plural': 'Faturalar',
                'db_table': 'Fatura',
            },
        ),
    ]

# Generated by Django 3.1.4 on 2021-01-08 12:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0003_taggeditem_add_unique_index'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, verbose_name='タイトル')),
                ('content', models.TextField(max_length=100, verbose_name='投稿内容')),
                ('site_link', models.CharField(blank=True, max_length=100, null=True, verbose_name='参考サイトへのリンク')),
                ('views', models.PositiveIntegerField(default=0, verbose_name='閲覧数')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='公開日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('like', models.ManyToManyField(blank=True, related_name='like', to=settings.AUTH_USER_MODEL, verbose_name='いいね')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post', to=settings.AUTH_USER_MODEL, verbose_name='ユーザー')),
            ],
            options={
                'verbose_name': '投稿',
                'verbose_name_plural': '投稿',
                'db_table': 'posts',
            },
        ),
    ]

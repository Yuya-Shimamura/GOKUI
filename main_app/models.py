from django.db import models
from accounts.models import User
from taggit.managers import TaggableManager


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='ユーザー', related_name='post')
    title = models.CharField('タイトル', max_length=20)
    tags = TaggableManager()
    content = models.TextField('投稿内容', max_length=100)
    site_link = models.CharField('参考サイトへのリンク', max_length=100, blank=True, null=True)
    views = models.PositiveIntegerField('閲覧数', default=0)
    created_at = models.DateTimeField('公開日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)
    like = models.ManyToManyField(User, related_name='like', verbose_name='いいね', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'posts'
        verbose_name = '投稿'
        verbose_name_plural = '投稿'

from django.db import models
from accounts.models import User
from taggit.managers import TaggableManager
from django.utils import timezone


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
    favorite = models.ManyToManyField(User, related_name='favorite', verbose_name='お気に入り', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Post'
        verbose_name = 'Post'
        verbose_name_plural = 'posts'

class Comment(models.Model):
    post = models.ForeignKey(Post, verbose_name='投稿', related_name='post_comment', on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name='ユーザー', related_name='comment_author', on_delete=models.CASCADE)
    text = models.TextField('コメント', max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    parent = models.ForeignKey('self', verbose_name='親コメント', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        ordering = ['-created_at']

    class Meta:
        db_table = 'Comment'
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
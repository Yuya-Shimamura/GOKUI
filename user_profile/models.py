from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='ユーザー', related_name='profile')
    title = models.CharField('タイトル', max_length=20, blank=True, null=True)
    introduction = models.TextField('自己紹介', max_length=120, blank=True, null=True)
    site_link = models.CharField('ウェブサイト', max_length=100, blank=True, null=True)
    avater_image = models.ImageField(upload_to='images', verbose_name='プロフィール画像', blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'Profile'
        verbose_name_plural = 'プロフィール'

@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    if kwargs['created']:
        profile = Profile.objects.get_or_create(user=kwargs['instance'])
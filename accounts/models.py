from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class Manager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField('ユーザー名', unique=True, max_length=20, blank=False)
    email = models.EmailField('メールアドレス', unique=True)
    followees = models.ManyToManyField(
        'User', verbose_name='フォロー中のユーザー', through='FriendShip',
        related_name='+', blank=True, through_fields=('follower', 'followee')
    )
    followers = models.ManyToManyField(
        'User', verbose_name='フォローされているユーザー', through='FriendShip', 
        related_name='+', blank=True, through_fields=('followee', 'follower')
    )

    objects = Manager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class FriendShip(models.Model):
    follower = models.ForeignKey('User', on_delete=models.SET_NULL, blank=True, null=True, related_name='followee_friendships')
    followee = models.ForeignKey('User', on_delete=models.SET_NULL, blank=True, null=True, related_name='follower_friendships')

    class Meta:
        unique_together = ('follower', 'followee')
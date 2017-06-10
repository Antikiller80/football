from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from tournaments.models import Club, Player


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    favorite_teams = models.ManyToManyField(Club, blank=True, related_name='clubs', verbose_name='Любимая команда')
    favorite_players = models.ManyToManyField(Player, blank=True, related_name='favorite_players', verbose_name='Любимый игрок')
    location = models.CharField('Страна', max_length=30, blank=True)
    birth_date = models.DateField('День рождения', null=True, blank=True)
    activation_key = models.CharField('Ключ активации', max_length=40, blank=True)
    key_expires = models.DateTimeField('Время деактивации', default=timezone.now)

    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#   for profile_instance in instance.profile_set.all():
#       profile_instance.save()

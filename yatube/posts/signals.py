from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.userprofile.save()  # Обращаемся к связанной модели UserProfile, а не к атрибуту 'profile' у User
    except UserProfile.DoesNotExist:
        # Если профиль пользователя не существует, создаем его
        UserProfile.objects.create(user=instance)

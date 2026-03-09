from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserPhone(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='phones')
    number = models.CharField(max_length=20, verbose_name="Номер телефону")
    is_verified = models.BooleanField(default=False, verbose_name="Підтверджено")

    def __str__(self):
        return f"{self.user.username}: {self.number}"

    class Meta:
        verbose_name = "Телефон користувача"
        verbose_name_plural = "Телефони користувачів"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True, verbose_name="Про себе")
    location = models.CharField(max_length=100, blank=True, verbose_name="Місто")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата народження")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="Аватар")

    def __str__(self):
        return f"Профіль: {self.user.username}"

    class Meta:
        verbose_name = "Профіль користувача"
        verbose_name_plural = "Профілі користувачів"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
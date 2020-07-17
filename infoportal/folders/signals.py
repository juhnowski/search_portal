from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import Folders


CustomUserModel = get_user_model()


@receiver(post_save, sender=CustomUserModel)
def create_root_folder(sender, instance, created, **kwargs):
    """
    сигнал, создание корневой folders после создания юзера
    """
    if created:
        user = CustomUserModel.objects.get(id=instance.id)
        name_folder = 'Избранное'
        Folders.objects.create(name=name_folder,
                               parent=None,
                               owner=user)
    else:
        pass

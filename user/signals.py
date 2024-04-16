from utils.utils import CommonUtils
from django.dispatch import receiver
from django.db import models
from .models import User
import logging 
logger = logging.getLogger( __name__ )

@receiver(models.signals.pre_delete, sender=User)
def delete_user(sender, instance, **kwargs):
    logger.info('deletion post user')
    if instance.avatar:
      # delete the avatar media from cloudinary
       CommonUtils.delete_media_from_cloudinary([instance.avatar])

    
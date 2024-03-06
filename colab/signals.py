from utils.utils import CommonUtils
from django.dispatch import receiver
from django.db import models
from .models import Colab
import logging 
logger = logging.getLogger( __name__ )

@receiver(models.signals.pre_delete, sender=Colab)
def delete_user(sender, instance, **kwargs):
    if instance.audio:
       CommonUtils.delete_media_from_cloudinary([instance.audio])
    
    if instance.video:
        CommonUtils.delete_media_from_cloudinary([instance.video])

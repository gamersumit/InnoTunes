from .models import User
import logging
from datetime import datetime, timedelta
from utils.utils import CommonUtils

logger = logging.getLogger( __name__ )


def remove_inactive_users():
    logger.info("\n----------------------------------------------------------------")
    logger.info("Cron job remove inactive user: %s", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
     # Calculate the datetime that was 30 days ago
    thirty_days_ago = datetime.now() - timedelta(days=30)
    # Filter users whose last deactivation date is before thirty_days_ago
    users = User.objects.filter(is_deleted = True, last_deactivation__lt=thirty_days_ago)

    for user in  users:
        CommonUtils.delete_media_from_cloudinary(user.avatar)
   
    logger.info("List of songs to be removed:")
    logger.info(str(users))
    users.delete()

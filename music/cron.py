from .models import RecentSongs
import logging
from datetime import datetime

logger = logging.getLogger( __name__ )


def remove_recent_songs():
    logger.info("\n----------------------------------------------------------------")
    logger.info("Cron job recent remove: %s", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    if RecentSongs.objects.all().count() > 10:
      recent_songs = RecentSongs.objects.filter().order_by('-last_played_at')
      recent_songs = list(recent_songs[10:])
      logger.info("List of songs to be removed:")
      logger.info(str(recent_songs))
      for song in recent_songs :
        song.delete()

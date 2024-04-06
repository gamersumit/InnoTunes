from .base import *

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "app_log_file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": 'log/app.log',
        },
    },
    "root": {
        "handlers": ["app_log_file"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["app_log_file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# cron job
CRONJOBS = [
    ('* */6 * * *', 'music.cron.remove_recent_songs'),
    ('* */6 * * *', 'user.cron.remove_inactive_users'),
]
import os

os.environ['DJANGO_SETTINGS_MODULE'] = "user_backend.settings"

import channels.asgi
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "user_backend.settings")
channel_layer = channels.asgi.get_channel_layer()

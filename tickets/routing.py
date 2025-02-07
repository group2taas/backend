from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # ticket_id (or any identifier) to identify the client
    re_path(r'ws/test_status/(?P<ticket_id>\w+)/$', consumers.TestStatusConsumer.as_asgi()),
]
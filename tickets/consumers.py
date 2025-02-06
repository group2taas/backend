# tickets/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class TestStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.ticket_id = self.scope['url_route']['kwargs']['ticket_id']
        self.group_name = f'test_status_{self.ticket_id}'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def test_status_update(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))

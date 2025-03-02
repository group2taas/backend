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
            'type': 'status_update',
            'message': message
        }))
        
    async def test_error(self, event):
        error = event['error']

        await self.send(text_data=json.dumps({
            'type': 'error',
            'error': error
        }))
        
    async def test_results_available(self, event):
        data = event['data']

        await self.send(text_data=json.dumps({
            'type': 'results_available',
            'data': data
        }))

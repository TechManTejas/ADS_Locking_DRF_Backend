# locking/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class LockingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Add the user to the locking group when they connect
        await self.channel_layer.group_add("locking_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Remove the user from the group when they disconnect
        await self.channel_layer.group_discard("locking_group", self.channel_name)

    async def receive(self, text_data):
        # Receive a message from the WebSocket client
        text_data_json = json.loads(text_data)
        event_type = text_data_json['event_type']
        seat_info = text_data_json['seat_info']

        # Broadcast the message to the locking_group
        await self.channel_layer.group_send(
            "locking_group",
            {
                'type': 'seat_update',  # Custom event type to broadcast
                'event_type': event_type,
                'seat_info': seat_info,
            }
        )

    async def seat_update(self, event):
        # Send the broadcasted seat update to the WebSocket client
        await self.send(text_data=json.dumps({
            'event_type': event['event_type'],
            'seat_info': event['seat_info'],
        }))

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room,Share

class ShareConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_code=self.scope['url_route']['kwargs']['room_code']
        self.group_name=f"room_{self.room_code}"

        await self.get_or_create_room(self.room_code)

        await self.channel_layer.group_add(self.group_name,self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name,self.channel_name)

    async def receive(self, text_data):
        data=json.loads(text_data)
        msg_type=data.get('type')

        if msg_type=='text':
            text=data.get('text_msg')
            share=await self.save_text(text)
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type':'share_message',
                    'payload':{
                        'type':'text','text_msg':text,'id':share.id
                    }
                }
            )  

    async def share_message(self, event):
        payload={k: v for k, v in event.items() if k != 'type'}
        await self.send(text_data=json.dumps(payload))

    @database_sync_to_async
    def get_or_create_room(self,code):
        room, _ = Room.objects.get_or_create(room_code=code)
        return room

    @database_sync_to_async
    def save_text(self,text):
        room=Room.objects.get(code=self.room_code)
        return Share.objects.create(room=room,text_msg=text)
    
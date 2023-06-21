import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.utils.text import slugify


class ChatConsumer(WebsocketConsumer):
    def connect(self):

        self.room_group_name = slugify(self.scope['url_route']['kwargs']['roomkey'])

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'ConnectActionInfo',
                'user': str(self.scope['user'])
            }
        )

    def ConnectActionInfo(self, event):
        self.send(text_data = json.dumps({
             
             'type': 'Connect',
             'Room': self.room_group_name,
             'Message': 'success',
             'msg': "User:" + " " + event['user'] + " " +"connected the chat"
        }))

    def disconnect(self, *args):
        async_to_sync(self.channel_layer.group_discard(self.room_group_name, self.channel_name))

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'DisconnectActionInfo',
                'user': str(self.scope['user'])
            }
        )

    def DisconnectActionInfo(self, event):
        self.send(text_data = json.dumps({
             
             'type': 'Disconnect',
             'Room': self.room_group_name,
             'Message': 'success',
             'msg': "User:" + " " + event['user'] + " " +"disconnected the chat"
        }))
    
    def receive(self, text_data):
        
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_msg',
                'message' : json.loads(text_data)['message'],  
                'user': str(self.scope['user'])
            }
        )
        
    def chat_msg(self, event):

          self.send(text_data= json.dumps(
           {
               'type': 'chat',
               'msg': event['message'],
               'user': str(event['user'])
           }   
          )) 
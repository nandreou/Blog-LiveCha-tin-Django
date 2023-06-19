import json
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        
        self.accept()

    def receive(self, text_data):
        self.send(text_data = json.dumps({
          'type':"chat",
          'msg': json.loads(text_data)['message'],
          'user': self.scope['user'].username
        }))
        
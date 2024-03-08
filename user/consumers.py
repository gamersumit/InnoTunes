# myapp/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
class UserConnectivityStatusConsumer(AsyncWebsocketConsumer):
    async def websocket_connect(self, event):
        try:
            print(self.scope)
            query_params = parse_qs(self.scope['query_string'].decode())
            token = query_params.get('token', [None])[0]
            from utils.utils import UserUtils
            user = await sync_to_async(UserUtils.getUserFromToken)(token)
            user.status = 'online' 
            await database_sync_to_async(user.save)() 
            self.scope['user'] = user
            await self.accept()

        except Exception as e:
            await self.close(code=4000, reason=str(e))

    async def websocket_receive(self, event):
        print('recevied')
        
    
    async def websocket_disconnect(self, event):
        user = self.scope.get('user')
        if user:
            user.status = 'offline'
            await database_sync_to_async(user.save)()  # Await and save


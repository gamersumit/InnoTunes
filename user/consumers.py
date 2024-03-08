# myapp/consumers.py
from channels.consumer import SyncConsumer, AsyncConsumer
from urllib.parse import parse_qs
from channels.db import database_sync_to_async
class UserConnectivityStatusConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        # try:
            print('conneting......')
            # query_params = parse_qs(self.scope['query_string'].decode())
            # token = query_params.get('token', [None])[0]
            # print(token)
            # from utils.utils import UserUtils
            # from .models import User
            # user = await UserUtils.getUserFromToken(token)
            # print(user.status)
            # user.status = 'online' 
            # await database_sync_to_async(user.save)() 
            # self.scope['user'] = user
            # print(user.status)
            await self.accept()

        # except Exception as e:
        #     pass
            # await self.close(code=4000, reason=str(e))

    async def websocket_receive(self, event):
        print('recevied')
        # Handle incoming WebSocket data
        
    
    async def websocket_disconnect(self, event):
        # user = self.scope.get('user')
        # if user:
        #     user.status = 'offline'
        #     await database_sync_to_async(user.save)()  # Await and save
        print('disconnect')


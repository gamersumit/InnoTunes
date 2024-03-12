from channels.consumer import SyncConsumer, AsyncConsumer
from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from channels.exceptions import StopConsumer
import json
   
        
class UserConnectivityStatusConsumer(AsyncConsumer):
    online_users = {}
    async def websocket_connect(self, event):
        try:
            print('connecting ...')
            query_params = parse_qs(self.scope['query_string'].decode())
            print(query_params)
            token = query_params.get('token', [None])[0]
            print(token)
            if not token:
                raise ValueError("Token not provided")
            
            from utils.utils import UserUtils  # Adjust import as needed
            print('fetching user')
            user = await sync_to_async(UserUtils.getUserFromToken)(token)
            print(user)
            if not user:
                raise ValueError("Invalid token")
            
            user.status = 'online'
            await database_sync_to_async(user.save)()
            
            self.user = user
            self.groupname = 'online_users_group'
            self.online_users[user.id] = {'user_id' : user.id}
            await self.channel_layer.group_add(
                self.groupname, #static group name
                self.channel_name
                )
            
            await self.send({
                'type': 'websocket.accept',
            })
            
            await self.channel_layer.group_send(self.groupname, {
            'type': 'broadcast.message',  # event , now we have to write handler for this event
            'message': json.dumps({'online' : user.id}),
            'sender': self.channel_name,
        })
            
        except Exception as e:
            print("error:", str(e))
            await self.close(code=4000, reason=str(e))   

    async def websocket_receive(self, event):
        print('Message Recieved...', event)
        print('message: ', event['text'])

    async def broadcast_message(self, event):
        print('broadcast')   
        if(event['sender'] != self.channel_name):
            await self.send({
                'type': 'websocket.send',
                'text': event['message'],
            })
            
        else:
            print('if same')
            await self.send({
                'type': 'websocket.send',
                'text': json.dumps({'connected' : self.online_users}),
            })
            
            

    async def websocket_disconnect(self, event):
        print('websocket Disconnected...', event)
        await self.channel_layer.group_discard(
            self.groupname,
            self.channel_name
        )
        self.user.status = 'offline'
        await database_sync_to_async(self.user.save)()
        self.online_users.pop(self.user.id, None) 
        await self.send({
                'type': 'websocket.send',
                'text': json.dumps({'offline' : self.user.id}),
            })           
        raise StopConsumer()

from email import message
from channels.consumer import SyncConsumer, AsyncConsumer
from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from channels.exceptions import StopConsumer
import json




   
        
class UserConnectivityStatusConsumer(AsyncConsumer):
    
    online_friends = set()
    
    async def websocket_connect(self, event):
        try:
            query_params = parse_qs(self.scope['query_string'].decode())
            token = query_params.get('token', [None])[0]
           
            if not token:
                raise ValueError("Token not provided")
            
            from utils.utils import UserUtils  # Adjust import as needed
            user = await sync_to_async(UserUtils.getUserFromToken)(token)
          
            if not user:
                raise ValueError("Invalid token")
            
            
            await self.send({
                'type': 'websocket.accept',
            })
            
            self.user = user
            self.groupname = f"group_{user.id}"
            print(self.online_friends)
            print('here0')
            from comment.models import Followers
            
            print('here1')
            friends = await sync_to_async(Followers.objects.filter)(artist_id = user.id)
            print('here2')
            friends = await sync_to_async(friends.values_list)('user_id', flat = True)
            print('here3')
            all_friends = await sync_to_async(list)(friends)
            print('here4')
 
            for friend in  all_friends :
                await self.channel_layer.group_add(
                    f"group_{friend}",
                    self.channel_name
                    )

            
            print('here7')

            self.user.status = 'online'
            await database_sync_to_async(self.user.save)()
            print('here8')
            
            
            await self.channel_layer.group_send(self.groupname, {
            'type': 'connect.user.status',  
            'text' : self.user.id,
            'sender': self.channel_name,
            
                                            })
        
            print('here9')
            from user.models import User
            friends = await sync_to_async(User.objects.filter)(id__in = friends, status = 'online')
            friends = await sync_to_async(friends.values_list)('id', flat = True)
            friends = await sync_to_async(list)(friends)
            
            await self.send({
                'type': 'websocket.send',
                'text': json.dumps({'connected' : friends}),
            })
            
        except Exception as e:
            print("error0:", str(e))
            await self.close(code=4000, reason=str(e))   

    async def websocket_receive(self, event):
        try : 
            print('reciveing ....')
            print(event)
            message = json.loads(event['text'])
            print(message)
            
            # Trigger currently_playing event
            await self.currently_playing({'text' : message['text'], 
            'sender': self.channel_name,
        })
            
       
            
        except Exception as e:
            print(str(e))
            await self.send({
                'type': 'websocket.send',
                'text': json.dumps({'error' : str(e)}),
            })
      
            
    async def connect_user_status(self, event):
        await self.send({
            'type': 'websocket.send',
            'text':  json.dumps({'online' : event['text']}),
        })
        
        
        
            
        # else:
        #     channels = await self.channel_layer.group_channels(self.groupname)
        #     await self.send({
        #         'type': 'websocket.send',
        #         'text': json.dumps({'connected' : channels}),
        #     })
    
    async def disconnect_user_status(self, event): 
        if(event['sender'] != self.channel_name):
            await self.send({
                'type': 'websocket.send',
                'text':  json.dumps({'offline' : event['text']}),
            })
            
    
    
    async def currently_playing(self, event):
        try : 
            print('current') 
            from music.models import Song
            song = await sync_to_async(Song.objects.get)(id = event['text']['song_id']) 
            print(song) 
            data = {'id' : song.id, 'song_name' : song.song_name, 'song_picture': song.song_picture}
            await self.channel_layer.group_send(self.groupname, {
            'type': 'broadcast.currently.playing',
            'text' : json.dumps({'currently_playing' : data, 'user_id' : self.user.id}), 
            'sender': self.channel_name,
             })
            
        
        except Exception as e:
            print(str(e))
            await self.send({
                    'type': 'websocket.send',
                    'text': json.dumps({'error' : str(e)}),
                })
            
            
    async def broadcast_currently_playing(self, event):
        if(event['sender'] != self.channel_name):
            await self.send({
                    'type': 'websocket.send',
                    'text': event['text'],
                })   
                 

    async def websocket_disconnect(self, event):
        
        try : 
            print('websocket Disconnected...', event)
            await self.channel_layer.group_discard(
                self.groupname,
                self.channel_name
            )
            
            self.user.status = 'offline'
            await database_sync_to_async(self.user.save)()
            
            await self.channel_layer.group_send(self.groupname, {
                'type': 'disconnect.user.status',  # event , now we have to write handler for this event
                'text':  self.user.id,
                'sender': self.channel_name,
            })
                
            raise StopConsumer()
        
        except Exception as e:
            print('error: ', str(e))

from calendar import c
from email import message
from channels.consumer import SyncConsumer, AsyncConsumer
from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async, async_to_sync
from channels.exceptions import StopConsumer
import json

        
class UserConnectivityStatusConsumer(AsyncConsumer):
    
    online_friends = set()
    
    @staticmethod
    def get_music_data(music):
        return music.song_id, music.user_id
    
    
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
            from comment.models import Followers
            
            friends = await sync_to_async(Followers.objects.filter)(user_id = user.id)
            friends = await sync_to_async(friends.values_list)('artist_id', flat = True)
            all_friends = await sync_to_async(list)(friends)
            
            print(all_friends)
            for friend in  all_friends :


                print(friend)
                groupname = f"group_{friend}"
                print(groupname)

                await self.channel_layer.group_add(
                    groupname,
                    self.channel_name
                    )
            
            self.user.status = 'online'
            await database_sync_to_async(self.user.save)()
            
            await self.channel_layer.group_send(self.groupname, {
            'type': 'connect.user.status',  
            'text' : self.user.id,
            'sender': self.channel_name,
            
                                            })
        
            from user.models import User
            friends = await sync_to_async(User.objects.filter)(id__in = friends, status = 'online')
            friends = await sync_to_async(friends.values_list)('id', flat = True)
            friends = await sync_to_async(list)(friends)
            
            from music.models import CurrentlyPlaying
            from music.serializers import CurrentlyPlayingSerializer
            
            currently_playing = await sync_to_async(CurrentlyPlaying.objects.filter)(pk__in = friends)
            currently_playing = await sync_to_async(list)(currently_playing)
            await sync_to_async(print)(currently_playing)
            data = []
            
            for music in currently_playing:
                song, user = await sync_to_async(UserConnectivityStatusConsumer.get_music_data)(music)
                data.append({
                    'song_name': song.song_name,
                    'song_picture': song.song_picture,
                    'song_id': song.id,
                    'user_id': user.id
                })
              
            await self.send({
                'type': 'websocket.send',
                'text': json.dumps({'connected' : friends, 'listening' : data}),
            })
           
        except Exception as e:
            await self.disconnect(code=4000, reason=str(e))   

    async def websocket_receive(self, event):
        try : 
            message = json.loads(event['text'])
           
            # Trigger currently_playing event
            await self.currently_playing({'text' : message['text'], 
            'sender': self.channel_name,
        })
            
       
            
        except Exception as e:
            await self.send({
                'type': 'websocket.send',
                'text': json.dumps({'error' : str(e)}),
            })
      
            
    async def connect_user_status(self, event):
        await self.send({
            'type': 'websocket.send',
            'text':  json.dumps({'online' : event['text']}),
        })
        
    
    async def disconnect_user_status(self, event): 
        if(event['sender'] != self.channel_name):
            await self.send({
                'type': 'websocket.send',
                'text':  json.dumps({'offline' : event['text']}),
            })
            
    
    
    async def currently_playing(self, event):
        from music.models import CurrentlyPlaying
        try : 
            from music.models import Song
            song = await sync_to_async(Song.objects.get)(id = event['text']['song_id']) 
            data = {'id' : song.id, 'song_name' : song.song_name, 'song_picture': song.song_picture}
            await self.channel_layer.group_send(self.groupname, {
            'type': 'broadcast.currently.playing',
            'text' : json.dumps({'currently_playing' : data, 'user_id' : self.user.id}), 
            'sender': self.channel_name,
             })
            
            currently_playing = None
            is_listening = await sync_to_async(CurrentlyPlaying.objects.filter)(user_id=self.user.id)
            is_listening = await sync_to_async(is_listening.exists)()
            if is_listening :
                currently_playing = await sync_to_async(CurrentlyPlaying.objects.filter)(user_id = self.user.id)
                currently_playing = await sync_to_async(currently_playing.first)()
                currently_playing.song_id = song 
                
                
            else :
                currently_playing = await sync_to_async(CurrentlyPlaying)(user_id = self.user, song_id = song)   

            await sync_to_async(currently_playing.save)()

            
            
        
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
        from music.models import CurrentlyPlaying
        try : 
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
            currently_playing = await sync_to_async(CurrentlyPlaying.objects.filter)(user_id = self.user.id)
            is_currently_playing = await sync_to_async(currently_playing.exists)()
            
            if is_currently_playing:
                await sync_to_async(currently_playing.delete)()
            raise StopConsumer()
        
        except Exception as e:
            print('error: ', str(e))

# myapp/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer

class UserConnectivityStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self, event):
        await self.accept()

    async def receive(self, event):
        # Handle incoming WebSocket data
        pass
    
    async def disconnect(self, event):
        pass  # Clean up if needed


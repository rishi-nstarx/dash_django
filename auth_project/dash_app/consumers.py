import json
from random import randint
from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio

class LiveDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the WebSocket connection
        await self.accept()
        print("Hey Rishi.........WS connection got established man.....")
        # Start the task for sending live data
        self.task = asyncio.create_task(self.send_live_data())

    async def disconnect(self, close_code):
        # Cancel the task to stop sending data when the WebSocket disconnects
        if hasattr(self, 'task'):
            self.task.cancel()
            print("Hey man you connection just got disconnected....")

    async def send_live_data(self):
        while True:
            zones = ["Zone A", "Zone B", "Zone C", "Zone D"]
            data = {zone: randint(500, 10000) for zone in zones}
            # Send data to the WebSocket
            await self.send(text_data=json.dumps(data))
            await asyncio.sleep(1)  # Adjust interval as needed

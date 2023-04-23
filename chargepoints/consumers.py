import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChargepointsConsumer(WebsocketConsumer):
    """Websocket consumer that allows all clients connected to receive notifications. Note that there is only one group
    called 'lobby', so all clients will receive all notifications.

    If you'd like to send a notification from somewhere in the code, you can do it like this:
        async_to_sync(get_channel_layer().group_send)(
                "lobby", {"type": "send_notification", "message": "<Your message here>"}
            )
    """

    def connect(self):
        # There is only one group called "lobby" where all clients are subscribed
        self.room_group_name = "lobby"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def send_notification(self, event):
        message = event["message"]
        self.send(text_data=json.dumps({"message": message}))

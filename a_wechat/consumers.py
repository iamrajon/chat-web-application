
from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync

from django.shortcuts import get_object_or_404
from a_wechat.models import ChatGroup, ChatGroupMessages
from django.template.loader import render_to_string
import json
from a_users.models import Profile


class ChatroomConsumer(WebsocketConsumer):
    
    def connect(self):

        # print("Connected with websocket..")
        # print("Channel Layer: ", self.channel_layer)
        # print("Channel Name: ", self.channel_name)

        self.user = self.scope['user']   # get request.user in consumer
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']  # get name of chatroom from url of websocket

        #get instance of ChatGroup model of that particular chatroom coming from websocket url
        self.chatroom = get_object_or_404(ChatGroup, group_name=self.chatroom_name)

        # adding channel_layer to group
        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name,
            self.channel_name
        )

        # add and update users
        if self.user not in self.chatroom.users_online.all():
            self.chatroom.users_online.add(self.user)
            self.update_online_count()


        self.accept()  # accept the websocket connection request


    def receive(self, text_data):

        # getting message body from json string being sent by client
        text_data_dict = json.loads(text_data)
        body = text_data_dict['body']
        print("Message from client: ", body)

        # saving message body to database table
        message = ChatGroupMessages.objects.create(
            body=body,
            author=self.user,
            group=self.chatroom
        )

        event = {
            "type": "message.handler",
            "message_id": message.id
        }

        # add message to group
        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name,
            event
        )
        
    # handler method for broadcasting message to every client in group
    def message_handler(self, event):
        message_id = event["message_id"]
        message = ChatGroupMessages.objects.get(id=message_id)

        context = {"message": message, "user": self.user}

        # broadcast data to group
        html = render_to_string("partials/_chat_message_p.html", context)
        self.send(text_data=html)




    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name,
            self.channel_name
        )

        # add and update users
        if self.user in self.chatroom.users_online.all():
            self.chatroom.users_online.remove(self.user)
            self.update_online_count()

        raise StopConsumer()
    

    # methods for adding and removing users
    def update_online_count(self):
        online_count = self.chatroom.users_online.count() - 1
        online_users = self.chatroom.users_online.all()
        other_user_queryset = self.chatroom.users_online.exclude(username=self.user.username)

        other_user_id = None
        if other_user_queryset.exists():  # Check if the queryset is not empty
            other_user = other_user_queryset.first()  # Get the first user
            other_user_id = other_user.id  # Get the ID of the other user

        event = {
            'type': 'online_count_handler',
            'online_count': online_count,
            'online_users': online_users,
            'other_user_id': other_user_id,
        }

        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name,
            event
        )

    # online count handler
    def online_count_handler(self, event):
        online_count = event['online_count']
        online_users = event['online_users']
        online_users_ids = [user.id for user in online_users]
        other_user_id = event['other_user_id']
        

        context = {
            'online_count': online_count,
            'online_users_ids': online_users_ids,
            'other_user_id': other_user_id,
            'other_profiles': Profile.objects.exclude(user=self.user)
        }
        html = render_to_string("partials/_online_count_p.html", context)
        self.send(text_data=html)






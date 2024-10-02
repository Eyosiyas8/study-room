from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Message, User, Chat


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = '__all__'

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']

class MyUserCreation(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2', 'avatar']

class ChatForm(ModelForm):
    class Meta:
        model = Chat
        fields = ['message']

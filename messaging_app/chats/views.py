from django.shortcuts import render
from chats.models import Conversation, Message, User
from chats.serializers import ConversationSerializer, MessageSerializer, UserSerializer

from rest_framework import viewsets
from rest_framework.permissions import AllowAny
# Create your views here.


class ConversationViewSet(viewsets.ModelViewSet):
    queryset =  Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [AllowAny]
    
    
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [AllowAny]
    
     
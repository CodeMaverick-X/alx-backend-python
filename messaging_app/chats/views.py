from django.shortcuts import render
from chats.models import Conversation, Message, User
from chats.serializers import ConversationSerializer, MessageSerializer, UserSerializer, MessageCreateSerializer

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response
# Create your views here.


class ConversationViewSet(viewsets.ModelViewSet):
    queryset =  Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['participants', 'created_at']
    
    @action(detail=False, methods=['post'])
    def create_conversation(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer) # Calls the create method of the serializer
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['conversation', 'sender', 'sent_at']
    
    @action(detail=False, methods=['post'])
    def send_message(self, request):
        # Use MessageCreateSerializer for sending messages as it's designed for this.
        # Pass the request context to the serializer for validation (e.g., current user)
        serializer = MessageCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save() # This calls the create method of MessageCreateSerializer
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
     
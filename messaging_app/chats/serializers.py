from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model with basic user information
    """
    class Meta:
        model = User
        fields = [
            'user_id', 
            'username', 
            'email', 
            'first_name', 
            'last_name', 
            'phone_number',
            'date_joined'
        ]
        read_only_fields = ['user_id', 'date_joined']


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for User model including conversation count
    """
    conversations_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'user_id',
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'date_joined',
            'conversations_count'
        ]
        read_only_fields = ['user_id', 'date_joined']
    
    def get_conversations_count(self, obj):
        return obj.conversations.count()


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message model
    """
    sender = UserSerializer(read_only=True)
    sender_id = serializers.UUIDField(write_only=True, source='sender.user_id')
    
    class Meta:
        model = Message
        fields = [
            'message_id',
            'message_body',
            'sent_at',
            'sender',
            'sender_id',
            'conversation'
        ]
        read_only_fields = ['message_id', 'sent_at']


class MessageCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating messages
    """
    class Meta:
        model = Message
        fields = [
            'message_body',
            'conversation',
            'sender'
        ]
    
    def create(self, validated_data):
        # Set sender from request context if not provided
        if 'sender' not in validated_data:
            validated_data['sender'] = self.context['request'].user
        return super().create(validated_data)


class ConversationSerializer(serializers.ModelSerializer):
    """
    Basic serializer for Conversation model
    """
    participants = UserSerializer(many=True, read_only=True)
    participants_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )
    messages_count = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'participants_ids',
            'created_at',
            'messages_count',
            'last_message'
        ]
        read_only_fields = ['conversation_id', 'created_at']
    
    def get_messages_count(self, obj):
        return obj.messages.count()
    
    def get_last_message(self, obj):
        last_message = obj.messages.last()
        if last_message:
            return {
                'message_body': last_message.message_body,
                'sent_at': last_message.sent_at,
                'sender': last_message.sender.username
            }
        return None
    
    def create(self, validated_data):
        participants_ids = validated_data.pop('participants_ids', [])
        conversation = Conversation.objects.create(**validated_data)
        
        if participants_ids:
            participants = User.objects.filter(user_id__in=participants_ids)
            conversation.participants.set(participants)
        
        return conversation


class ConversationDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for Conversation model including nested messages
    """
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    participants_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'participants_ids',
            'messages',
            'created_at'
        ]
        read_only_fields = ['conversation_id', 'created_at']
    
    def create(self, validated_data):
        participants_ids = validated_data.pop('participants_ids', [])
        conversation = Conversation.objects.create(**validated_data)
        
        if participants_ids:
            participants = User.objects.filter(user_id__in=participants_ids)
            conversation.participants.set(participants)
        
        return conversation


class ConversationListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing conversations with minimal data
    """
    participants = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'created_at',
            'last_message',
            'unread_count'
        ]
    
    def get_participants(self, obj):
        # Return participant names excluding current user
        current_user = self.context.get('request').user if self.context.get('request') else None
        participants = obj.participants.exclude(user_id=current_user.user_id) if current_user else obj.participants.all()
        return [participant.username for participant in participants]
    
    def get_last_message(self, obj):
        last_message = obj.messages.last()
        if last_message:
            return {
                'message_body': last_message.message_body[:50] + '...' if len(last_message.message_body) > 50 else last_message.message_body,
                'sent_at': last_message.sent_at,
                'sender': last_message.sender.username
            }
        return None
    
    def get_unread_count(self, obj):
        # This would require a read status model to implement properly
        # For now, return 0 as placeholder
        return 0
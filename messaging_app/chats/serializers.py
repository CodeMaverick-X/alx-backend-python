from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model with basic user information
    """
    full_name = serializers.CharField(read_only=True)
    
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
            'full_name'
        ]
        read_only_fields = ['user_id', 'date_joined']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()
    
    def validate_username(self, value):
        """
        Custom validation for username
        """
        if len(value) < 3:
            raise serializers.ValidationError("Username must be at least 3 characters long.")
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value
    
    def validate_phone_number(self, value):
        """
        Custom validation for phone number
        """
        if value and not value.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise serializers.ValidationError("Phone number must contain only digits, spaces, hyphens, and plus signs.")
        return value


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
    sender_name = serializers.CharField(source='sender.username', read_only=True)
    
    class Meta:
        model = Message
        fields = [
            'message_id',
            'message_body',
            'sent_at',
            'sender',
            'sender_id',
            'sender_name',
            'conversation'
        ]
        read_only_fields = ['message_id', 'sent_at']
    
    def validate_message_body(self, value):
        """
        Custom validation for message body
        """
        if not value or not value.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        if len(value) > 1000:
            raise serializers.ValidationError("Message body cannot exceed 1000 characters.")
        return value.strip()


class MessageCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating messages
    """
    conversation_id = serializers.CharField(write_only=True)
    
    class Meta:
        model = Message
        fields = [
            'message_body',
            'conversation_id',
            'sender'
        ]
    
    def validate_message_body(self, value):
        """
        Validate message content
        """
        if not value or not value.strip():
            raise serializers.ValidationError("Message cannot be empty.")
        return value.strip()
    
    def validate_conversation_id(self, value):
        """
        Validate that conversation exists and user is a participant
        """
        try:
            conversation = Conversation.objects.get(conversation_id=value)
        except Conversation.DoesNotExist:
            raise serializers.ValidationError("Conversation does not exist.")
        
        # Check if user is a participant in the conversation
        request = self.context.get('request')
        if request and request.user not in conversation.participants.all():
            raise serializers.ValidationError("You are not a participant in this conversation.")
        
        return value
    
    def create(self, validated_data):
        # Set sender from request context if not provided
        if 'sender' not in validated_data:
            validated_data['sender'] = self.context['request'].user
        
        # Get conversation from conversation_id
        conversation_id = validated_data.pop('conversation_id')
        conversation = Conversation.objects.get(conversation_id=conversation_id)
        validated_data['conversation'] = conversation
        
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
    participants_names = serializers.CharField(read_only=True)
    messages_count = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'participants_ids',
            'participants_names',
            'created_at',
            'messages_count',
            'last_message'
        ]
        read_only_fields = ['conversation_id', 'created_at']
    
    def get_participants_names(self, obj):
        return ", ".join([user.username for user in obj.participants.all()])
    
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
    
    def validate_participants_ids(self, value):
        """
        Validate participants list
        """
        if len(value) < 1:
            raise serializers.ValidationError("A conversation must have at least one participant.")
        if len(value) > 50:
            raise serializers.ValidationError("A conversation cannot have more than 50 participants.")
        
        # Check if all participants exist
        existing_users = User.objects.filter(user_id__in=value)
        if len(existing_users) != len(value):
            raise serializers.ValidationError("One or more participants do not exist.")
        
        return value
    
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
    conversation_title = serializers.CharField(read_only=True)
    
    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'participants_ids',
            'messages',
            'conversation_title',
            'created_at'
        ]
        read_only_fields = ['conversation_id', 'created_at']
    
    def get_conversation_title(self, obj):
        """
        Generate a title for the conversation based on participants
        """
        participants = obj.participants.all()
        if len(participants) == 2:
            return f"Chat between {participants[0].username} and {participants[1].username}"
        elif len(participants) > 2:
            return f"Group chat with {len(participants)} participants"
        return "Empty conversation"
    
    def validate_participants_ids(self, value):
        """
        Validate participants for conversation creation
        """
        if not value:
            raise serializers.ValidationError("Participants list cannot be empty.")
        
        if len(set(value)) != len(value):
            raise serializers.ValidationError("Duplicate participants are not allowed.")
        
        # Validate that all participants exist
        existing_count = User.objects.filter(user_id__in=value).count()
        if existing_count != len(value):
            raise serializers.ValidationError("One or more participants do not exist.")
        
        return value
    
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
    participants_names = serializers.CharField(read_only=True)
    last_message_preview = serializers.CharField(read_only=True)
    unread_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants_names',
            'created_at',
            'last_message_preview',
            'unread_count'
        ]
    
    def get_participants_names(self, obj):
        # Return participant names excluding current user
        current_user = self.context.get('request').user if self.context.get('request') else None
        participants = obj.participants.exclude(user_id=current_user.user_id) if current_user else obj.participants.all()
        return ", ".join([participant.username for participant in participants])
    
    def get_last_message_preview(self, obj):
        last_message = obj.messages.last()
        if last_message:
            preview = last_message.message_body[:50] + '...' if len(last_message.message_body) > 50 else last_message.message_body
            return f"{last_message.sender.username}: {preview}"
        return "No messages yet"
    
    def get_unread_count(self, obj):
        # This would require a read status model to implement properly
        # For now, return 0 as placeholder
        return 0
    
    def validate(self, data):
        """
        Object-level validation
        """
        # Add any cross-field validation here if needed
        return data
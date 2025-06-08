import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Extension of Django's AbstractUser to add custom fields
    """
    # AbstractUser already includes: username, email, first_name, last_name,
    # is_active, is_staff, is_superuser, date_joined, last_login, password
    
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return self.username

class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        user_list = ", ".join([user.username for user in self.participants.all()[:2]])
        return f"Conversation: {user_list}"
    
    class Meta:
        ordering = ['-created_at']

class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message_body = models.TextField()  # Changed from 'content' to 'message_body'
    sent_at = models.DateTimeField(auto_now_add=True)  # Changed from 'created_at' to 'sent_at'
    conversation = models.ForeignKey(
        Conversation, 
        on_delete=models.CASCADE, 
        related_name='messages',
        null=True,
        blank=True
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    
    def __str__(self):
        return f"{self.sender.username}: {self.message_body[:50]}..."
    
    class Meta:
        ordering = ['sent_at']
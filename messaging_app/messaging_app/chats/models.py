from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Extension of Django's AbstractUser to add custom fields
    """
    # AbstractUser already includes: username, email, first_name, last_name, 
    # is_active, is_staff, is_superuser, date_joined, last_login, password
    
    
    def __str__(self):
        return self.username

class Conversation(models.Model):
    users = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        user_list = ", ".join([user.username for user in self.users.all()[:2]])
        return f"Conversation: {user_list}"
    
    class Meta:
        ordering = ['-created_at']

class Message(models.Model):
    content = models.TextField()  # Use TextField for potentially longer messages
    created_at = models.DateTimeField(auto_now_add=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages' ,         null=True,  # Add this temporarily
        blank=True  # Add this temporarily
        )
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    
    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}..."
    
    class Meta:
        ordering = ['created_at']
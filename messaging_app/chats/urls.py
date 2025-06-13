from django.urls import path, include
from . import views
from rest_framework import routers

urlpatterns = [
    
]

router = routers.DefaultRouter()
router.register('conversations', views.ConversationViewSet)
router.register('messages', views.MessageViewSet)

urlpatterns += router.urls
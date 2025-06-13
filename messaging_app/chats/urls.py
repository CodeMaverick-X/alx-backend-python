from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    
]

router = DefaultRouter()
router.register('conversations', views.ConversationViewSet)
router.register('messages', views.MessageViewSet)

urlpatterns += router.urls
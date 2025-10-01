from django.urls import path
from .views import ConversationView, MessageView, MessagesLogView

urlpatterns = [
    path('conversations/', view=ConversationView.as_view(), name='conversations'),
    path('message/', view=MessageView.as_view(), name='messages'),
    path('message/log/', view=MessagesLogView.as_view(), name='messages-log')
]

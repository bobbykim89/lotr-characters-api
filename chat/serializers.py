from rest_framework import serializers
from .models import Conversation, Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "question", "answer", "feedback", "created_at"]

class MessageFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["feedback"]
    
    def validate_feedback(self, value):
        if value not in ["GOOD", "BAD"]:
            raise serializers.ValidationError("Feedback must be either 'GOOD' or 'BAD'")
        return value

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ["id", "created_at", "messages"]
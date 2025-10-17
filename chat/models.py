from django.db import models
import uuid

# Create your models here.
class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id}"
    
class Message(models.Model):
    FEEDBACK_CHOICES = [
        ("GOOD", "Good"),
        ("BAD", "Bad")
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, related_name="messages", on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    feedback = models.CharField(max_length=4, choices=FEEDBACK_CHOICES, null=True, blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"({self.conversation.id}) {self.question}: {self.answer[:50]}"
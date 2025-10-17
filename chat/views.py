from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_list_or_404, get_object_or_404

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer, MessageFeedbackSerializer
from lib.rag import LotrCharactersRag

# Create your views here.
class ConversationView(APIView):
    """
    GET:
        - If conversation_id provided, return its history
        - If not, create new conversation with default assistant message
    """
    def get(self, request):
        conversation_id = request.query_params.get("conversation_id")
        if conversation_id:
            conversation = get_object_or_404(Conversation, id=conversation_id)
            message = f"Successfully loaded conversation with id: {conversation_id}"
        else:
            conversation = Conversation.objects.create()
            message = "Ask any question about characters of Lord of the Rings!"

        serializer = ConversationSerializer(conversation)
        res = {
            "data": serializer.data,
            "message": message
        }
        return Response(data=res, status=status.HTTP_200_OK)

class MessageView(APIView):
    """
    POST:
        - Run RAG pipeline to generate assistant reply
        - Save user question and assistant answer into message object
        - Return message object
    """
    def post(self, request):
        conversation_id = request.data.get("conversation_id")
        question = request.data.get("question")

        if not conversation_id or not question:
            return Response(
                data={"error": "conversation_id and question are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        conversation = get_object_or_404(Conversation, id=conversation_id)

        # get answer from RAG
        lotr_rag = LotrCharactersRag()
        answer = lotr_rag.answer_lotr(query=question)

        # save message
        message = Message.objects.create(
            conversation=conversation,
            question=question,
            answer=answer
        )

        return Response(
            data={
                "conversation_id": str(conversation.id),
                "data": MessageSerializer(message).data,
            },
            status=status.HTTP_200_OK
        )
    
class MessagesLogView(ListAPIView):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

class MessageFeedbackUpdateView(UpdateAPIView):
    """
    Update feedback for a specific message
    """
    queryset = Message.objects.all()
    serializer_class = MessageFeedbackSerializer
    lookup_field = "id"
    lookup_url_kwarg = "message_id"
    http_method_names = ['put']
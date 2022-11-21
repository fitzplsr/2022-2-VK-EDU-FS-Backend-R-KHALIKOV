from django.http import JsonResponse, HttpRequest, HttpResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from chats.models import Chat
from .models import Message
from users.models import User
from django.utils import timezone


@csrf_exempt
@require_http_methods(['POST'])
def new_message(request):
    chat_id = request.POST.get('chat_id')
    sender_id = request.POST.get('sender_id')
    content = request.POST.get('content')
    if not (chat_id and sender_id and content):
        return JsonResponse(status=400, data={"Error": "No required attribute"})
    if not chat_id.isdigit() and sender_id.isdigit():
        return JsonResponse(status=400, data={"Error": "Not number in chat_id or user_id"})
    chat = get_object_or_404(Chat, pk=chat_id)
    sender = get_object_or_404(chat.users, pk=sender_id)
    Message.objects.create(
        chat=chat,
        sender=sender,
        content=content,
        )
    return JsonResponse(status=201, data={"Done": "Message was created"})


@require_http_methods(['GET'])
def message_detail(request):
    message_id = request.GET.get('message_id')
    if not message_id:
        JsonResponse(status=400, data={"Error": "No message_id"})
    if not message_id.isdigit():
        JsonResponse(status=400, data={"Error": "No number in message_id"})
    message_object = get_object_or_404(Message, pk=message_id)
    sender = message_object.sender
    chat = message_object.chat
    response = {
        'message_id': message_id,
        'content': message_object.content,
        'sender': {
            'id': sender.id,
            'name': sender.name,
                },
        'chat': {
            'id': chat.id,
            'users': list(chat.users.values('id', 'name')),
                },
    }
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(['POST'])
def edit_message(request):
    message_id = request.POST.get('message_id')
    content = request.POST.get('content')
    if not (message_id and content):
        return JsonResponse(status=400, data={"Error": "No required attribute"})
    if not message_id.isdigit():
        return JsonResponse(status=400, data={"Error": "No number in attribute"})
    message_object = get_object_or_404(Message, pk=message_id)
    current_content = message_object.content
    if current_content == content:
        return JsonResponse(status=400, data={"Error": "Nothing to edit"})
    message_object.content = content
    message_object.is_editing = True
    message_object.save()
    return JsonResponse(status=201, data={"Done": "Message has been edited"})


@require_http_methods(['GET'])
def read_message(request):
    message_id = request.GET.get('message_id')
    if not message_id:
        return JsonResponse(status=400, data={"Error": "No message_id"})
    if not message_id.isdigit():
        return JsonResponse(status=400, data={"Error": "Not number in message_id"})
    message_object = get_object_or_404(Message, pk=message_id)
    message_object.is_reading = True
    message_object.save()
    return JsonResponse(status=201, data={"Done": "Message has been read"})


@require_http_methods(['GET'])
def delete_message(request):
    message_id = request.GET.get('message_id')
    if not message_id:
        return JsonResponse(status=400, data={"Error": "No message_id"})
    if not message_id.isdigit():
        return JsonResponse(status=400, data={"Error": "Not number in message_id"})
    message_object = get_object_or_404(Message, pk=message_id)
    message_object.delete()
    return JsonResponse(status=201, data={"Done": "Message has been deleted"})

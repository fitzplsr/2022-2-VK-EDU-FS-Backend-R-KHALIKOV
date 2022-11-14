from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from django.db import connection
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
    if not chat_id.isdigit() and sender_id.isdigit():
        return HttpResponse(status=400, content="Not number in chat_id or user_id")
    chat = Chat.objects.filter(id=chat_id).last()
    if not chat:
        return HttpResponse(status=400, content='Chat does not exist')
    user_exist = User.objects.filter(id=sender_id).exists()
    if not user_exist:
        return HttpResponse(status=400, content='User does not exist')
    sender = chat.users.filter(id=sender_id).last()
    if not sender:
        return HttpResponse(status=400, content='This user is not from this chat')
    if not content:
        return HttpResponse(status=400, content='Can\'t create empty message')
    Message.objects.create(
        chat=chat,
        sender=sender,
        content=content,
        creating_time=timezone.localtime(timezone.now()))
    return HttpResponse(status=201, content="Message was created")


@require_http_methods(['GET'])
def message_detail(request):
    message_id = request.GET.get('id', None)
    if not message_id.isdigit():
        return HttpResponse(status=400, content="Not number in chat_id")
    message_id = int(message_id)
    message_object = Message.objects.filter(id=message_id).last()
    if not message_object:
        return HttpResponse(status=404, content='Message not found')
    sender = message_object.sender
    chat = message_object.chat
    chat_dict = {
        'id': chat.id,
        'users': list(chat.users.values('id', 'name')),
    }
    sender_dict = {
        'id': sender.id,
        'name': sender.name,
    }
    response = {
        'message_id': message_id,
        'chat': chat_dict,
        'sender': sender_dict,
    }
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(['POST'])
def message_edit(request):
    message_id = request.POST.get('id')
    content = request.POST.get('content')
    if not message_id.isdigit():
        return HttpResponse(status=400, content="Not number in message_id")
    if not content:
        return HttpResponse(status=400, content='You can\'t make empty message')
    message_object = Message.objects.filter(id=message_id)
    if not message_object:
        return HttpResponse(status=404, content='Message doesn\'t exist')
    current_content = message_object.last().content
    if current_content == content:
        return HttpResponse(status=400, content='Nothing to edit')
    message_object.update(content=content, creating_time=timezone.localtime(timezone.now()))
    return HttpResponse(status=201, content='Message edited')


@require_http_methods(['GET'])
def message_delete(request):
    message_id = request.GET.get('id')
    if not message_id.isdigit():
        return HttpResponse(status=400, content="Not number in message_id")
    message_object = Message.objects.filter(id=message_id)
    if not message_object:
        return HttpResponse(status=404, content='Message doesn\'t exist')
    message_object.delete()
    return HttpResponse(status=201, content='Message deleted')

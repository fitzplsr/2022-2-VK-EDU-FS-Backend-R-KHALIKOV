from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from chats.models import Chat
from .models import User


#http://localhost:8000/chats_list/messages/?id=3
@require_http_methods(['GET'])
def user_chats(request):
    user_id = request.GET.get('id', None)
    if not user_id.isdigit():
        return HttpResponse(status=400, content="Not number in user_id")
    user_id = int(user_id)
    user_object = User.objects.filter(id=user_id).last()
    if user_object:
        chats = user_object.chats.all()
    else:
        return HttpResponse(status=404, content='User not found')
    chats_lst = []
    for chat in chats:
        chats_lst.append(dict(chat_id=chat.id,
                              chat_users=list(chat.users.values('id', 'name'))))
    user_info = {
        'id': user_object.id,
        'name': user_object.name,
    }
    response = {
        'user': user_info,
        'chats': chats_lst,
    }
    return JsonResponse(response)


#http://localhost:8000/users/messages/?id=3&chat_id=1
@require_http_methods(['GET'])
def user_messages(request):
    user_id = request.GET.get('id', None)
    chat_id = request.GET.get('chat_id', None)
    if not chat_id.isdigit() and user_id.isdigit():
        return HttpResponse(status=400, content="Not number in chat_id or user_id")
    user_id = int(user_id)
    chat_id = int(chat_id)
    chat_object = Chat.objects.filter(id=chat_id).last()
    user_object = User.objects.filter(id=user_id).last()
    if not user_object:
        return HttpResponse(status=404, content='User not found')
    elif not chat_object:
        return HttpResponse(status=404, content='Chat not found')
    messages_objects = chat_object.messages.filter(sender__id=user_id)
    if not messages_objects:
        return HttpResponse(status=404, content='Messages not found')
    messages_lst = []
    for message in messages_objects:
        messages_lst.append(dict(sending_time=message.creating_time, content=message.content))
    user_info = {
        'id': user_object.id,
        'name': user_object.name,
    }
    chat_info = {
        'id': chat_object.id,
        'users': list(chat_object.users.values('id', 'name')),
    }
    response = {
        'user': user_info,
        'chat': chat_info,
        'message': messages_lst,
    }
    return JsonResponse(response)

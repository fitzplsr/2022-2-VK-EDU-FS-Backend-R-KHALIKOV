from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, get_list_or_404
from chats.models import Chat
from .models import User


@require_http_methods(['GET'])
def user_info(request):
    user_id = request.GET.get('user_id')
    if not user_id:
        return JsonResponse(status=400, data={"Error": "No user_id"})
    if not user_id.isdigit():
        return JsonResponse(status=400, data={"Error": "Not number in user_id"})
    user = get_object_or_404(User, pk=user_id)
    response = {
        'id': user.id,
        'name': user.name,
        'nickname': user.nickname,
        'birthday': user.birthday,
        'count_of_chats': len(user.chats.values())
    }
    return JsonResponse(response)


#http://localhost:8000/users/chats_list/messages/?id=3
@require_http_methods(['GET'])
def user_chats(request):
    user_id = request.GET.get('user_id')
    if not user_id.isdigit():
        return JsonResponse(status=400, data={"Error": "Not number in user_id"})
    user_object = get_object_or_404(User, pk=user_id)
    chats = user_object.chats.all()
    chats_lst = []
    for chat in chats:
        chats_lst.append(dict(chat_id=chat.id,
                              chat_users=list(chat.users.values('id', 'name')))
                         )
    if not chats:
        chats_lst.append("User has no chats")
    response = {
        'user': {
                'id': user_object.id,
                'name': user_object.name,
                },
        'chats': chats_lst,
    }
    return JsonResponse(response)


#http://localhost:8000/users/messages/?id=3&chat_id=1
@require_http_methods(['GET'])
def user_messages(request):
    user_id = request.GET.get('user_id')
    chat_id = request.GET.get('chat_id')
    if not (user_id and chat_id):
        return JsonResponse(status=400, data={"Error": "Not chat_id or user_id"})
    if not (chat_id.isdigit() and user_id.isdigit()):
        return JsonResponse(status=400, data={"Error": "Not number in chat_id or user_id"})
    chat_object = get_object_or_404(Chat, pk=chat_id)
    user_object = get_object_or_404(User, pk=user_id)
    messages_objects = get_list_or_404(chat_object.message, sender__id=user_id)
    messages_lst = []
    for message in messages_objects:
        messages_lst.append(dict(sending_time=message.creating_time, content=message.content))
    response = {
        'user': {
                'id': user_object.id,
                'name': user_object.name,
                },
        'chat': {
                'id': chat_object.id,
                'users': list(chat_object.users.values('id', 'name'))
                },
        'message': messages_lst,
    }
    return JsonResponse(response)

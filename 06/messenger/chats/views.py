from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404, get_list_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Chat
from users.models import User


@require_http_methods(['GET'])
def menu(request):
    return render(request, "index.html")


@csrf_exempt
@require_http_methods(['POST'])
def new_chat(request):
    title = request.POST.get('title')
    description = request.POST.get('description')
    if title:
        Chat.objects.create(title=title, description=description)
        return JsonResponse(status=201, data={"Done":"Chat was created"})
    return JsonResponse(status=400, data=({"Error": "No title of chat"}))


@require_http_methods(['GET'])
def delete_chat(request):
    chat_id = request.GET.get('id')
    if not chat_id.isdigit():
        return HttpResponse(status=400, content="Not number in chat_id")
    chat_object = get_object_or_404(Chat, pk=chat_id)
    chat_object.delete()
    return JsonResponse(status=200, content={"Done": "Chat was deleted"})


@require_http_methods(['GET'])
def show_chats(request):
    chats_dict = {}
    for chat in Chat.objects.all():
        chats_dict.update({
            f'chat_id_{chat.id}': {
                'title': chat.title,
                'description': chat.description,
                'creating_time': chat.creating_time,
                'editing_time': chat.editing_time,
                'users': list(chat.users.values('id', 'name')),
            }
        })
    return JsonResponse(chats_dict)


@require_http_methods(['GET'])
def chat_detail(request):
    chat_id = request.GET.get('chat_id')
    if not chat_id:
        return JsonResponse(status=400, data={"Error": "No chat_id"})
    if not chat_id.isdigit():
        return JsonResponse(status=400, data={"Error": "Not number in chat_id"})
    chat = get_object_or_404(Chat, pk=chat_id)
    users = list(chat.users.values('id', 'name'))
    response = {
        'chat_id': chat_id,
        'title': chat.title,
        'description': chat.description,
        'creating_time': chat.creating_time,
        'users': users
    }
    return JsonResponse(response)


@require_http_methods(['GET'])
def chat_messages(request):
    chat_id = request.GET.get('chat_id')
    if not chat_id:
        return JsonResponse(status=400, data={"Error": "No chat_id"})
    if not chat_id.isdigit():
        return JsonResponse(status=400, data={"Error": "Not number chat_id"})
    chat = get_object_or_404(Chat, pk=chat_id)
    messages_objects = get_list_or_404(chat.message)
    messages = []
    for message in messages_objects:
        messages.append(dict(
            sender_name=message.sender.name,
            content=message.content,
            creating_time=message.creating_time,
            is_editing=message.is_editing,
        ))
    return JsonResponse({"Messages": messages})

@csrf_exempt
@require_http_methods(['POST'])
def edit_chat(request):
    chat_id = request.POST.get('chat_id')
    title = request.POST.get('title')
    description = request.POST.get('description')
    if not chat_id:
        return JsonResponse(status=400, data={"Error": "No chat_id"})
    if not (title or description):
        return JsonResponse(status=400, data={"Error": "Nothing to edit"})
    if not chat_id.isdigit():
        return JsonResponse(status=400, data={"Error": "No number in chat_id"})
    chat_object = get_object_or_404(Chat, pk=chat_id)
    chat_object.title = title
    chat_object.descripton = description
    chat_object.save()
    return JsonResponse(status=201, data={"Done": "Chat has been edited"})

@require_http_methods(['GET'])
def delete_user(request):
    chat_id = request.GET.get('chat_id')
    user_id = request.GET.get('user_id')
    if not (chat_id and user_id):
        return JsonResponse(status=400, data={"Error": "No chat_id or user_id"})
    if not (chat_id.isdigit() and user_id.isdigit()):
        return JsonResponse(status=400, data={"Error": "Not number in chat_id or user_id"})
    chat = get_object_or_404(Chat, pk=chat_id)
    user = get_object_or_404(chat.users, pk=user_id)
    chat.users.remove(user)
    return JsonResponse(status=201, data={"Done": "User was deleted from chat"})


@require_http_methods(['GET'])
def add_user(request):
    chat_id = request.GET.get('chat_id')
    user_id = request.GET.get('user_id')
    if not (chat_id and user_id):
        return JsonResponse(status=400, data={"Error": "No chat_id or user_id"})
    if not (chat_id.isdigit() and user_id.isdigit()):
        return JsonResponse(status=400, data={"Error": "Not number in chat_id or user_id"})
    chat = get_object_or_404(Chat, pk=chat_id)
    user = get_object_or_404(User, pk=user_id)
    if chat.users.filter(id=user_id).exists():
        return JsonResponse(status=400, data={"Error": "User already in chat"})
    chat.users.add(user)
    return JsonResponse(status=201, data={"Done": "User was added to chat"})

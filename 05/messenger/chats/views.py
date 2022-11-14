from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Chat
from users.models import User


@require_http_methods(['GET'])
def menu(request):
    return render(request, "index.html")


@csrf_exempt
@require_http_methods(['POST'])
def new_chat(request):
    user_id_1 = request.POST.get('user_1') #body form-data
    user_id_2 = request.POST.get('user_2')
    if not user_id_1.isdigit() and user_id_2.isdigit():
        return HttpResponse(status=400, content="Not number in user_id")
    if user_id_1 == user_id_2:
        return HttpResponse(status=400, content="Can't create chat with 1 user")
    user_1 = User.objects.filter(id=user_id_1).last()
    user_2 = User.objects.filter(id=user_id_2).last()
    if user_1 and user_2:
        if User.objects.filter(id__in=[user_id_1, user_id_2]).last().chats.all():
            return HttpResponse(status=404, content="Chat already exists")
    if user_id_1 and user_id_2:
        chat = Chat.objects.create()
        chat.users.add(user_1, user_2)
        return HttpResponse(status=201, content="Chat was created")
    return HttpResponse(status=404, content="Not Found attribute")


@require_http_methods(['GET'])
def show_chats(request):
    chats_dict = {}
    for chat in Chat.objects.all():
        chat_id = chat.id
        chats_dict[chat_id] = []
        for user in Chat.objects.get(id=chat_id).users.all():
            chats_dict[chat_id].append(dict(user_id=user.id, user_name=user.name))
    return JsonResponse(chats_dict)


@require_http_methods(['GET'])
def chat_detail(request):
    chat_id = request.GET.get('id', None)
    if not chat_id.isdigit():
        return HttpResponse(status=400, content="Not number in chat_id")
    chat_id = int(chat_id)
    chat = Chat.objects.filter(id=chat_id).last()
    if not chat:
        return HttpResponse(status=404, content='Chat not found')
    users_objects = chat.users.all()
    messages_objects = chat.messages.all()
    users = []
    for user in users_objects:
        users.append(dict(user_id=user.id, user_name=user.name))
    messages = []
    for message in messages_objects:
        messages.append(dict(sender_name=message.sender.name, content=message.content))
    response = {
        'chat_id': chat_id,
        'users': users,
        'message': messages
    }
    return JsonResponse(response)


@require_http_methods(['GET'])
def delete_user(request):
    chat_id = request.GET.get('id')
    user_id = request.GET.get('user_id')
    if not chat_id.isdigit() and user_id.isdigit():
        return HttpResponse(status=400, content="Not number in chat_id or user_id")
    chat_id = int(chat_id)
    user_id = int(user_id)
    chat = get_object_or_404(Chat, pk=chat_id)
    if not chat:
        return HttpResponse(status=404, content='Chat not found')
    user = get_object_or_404(User, pk=user_id)
    if not user:
        return HttpResponse(status=404, content='User not found')
    user_in_chat = chat.users.filter(id=user_id).exists()
    if not user_in_chat:
        return HttpResponse(status=404, content='User not in chat')
    chat.users.remove(user)
    return HttpResponse(status=200, content='User was deleted from chat')


@require_http_methods(['GET'])
def add_user(request):
    chat_id = request.GET.get('id')
    user_id = request.GET.get('user_id')
    if not chat_id.isdigit() and user_id.isdigit():
        return HttpResponse(status=400, content="Not number in chat_id or user_id")
    chat_id = int(chat_id)
    user_id = int(user_id)
    chat = Chat.objects.filter(id=chat_id).last()
    if not chat:
        return HttpResponse(status=404, content='Chat not found')
    user = User.objects.filter(id=user_id).last()
    if not user:
        return HttpResponse(status=404, content='User doesn\'t exist')
    user_in_chat = chat.users.filter(id=user_id).exists()
    if user_in_chat:
        return HttpResponse(status=404, content='User already in chat')
    chat.users.add(user)
    return HttpResponse(status=200, content='User was added to chat')


@require_http_methods(['GET'])
def chat_delete(request):
    chat_id = request.GET.get('id')
    if not chat_id.isdigit():
        return HttpResponse(status=400, content="Not number in chat_id")
    chat_object = Chat.objects.filter(id=chat_id)
    if not chat_object:
        return HttpResponse(status=404, content='Chat doesn\'t exist')
    chat_object.delete()
    return HttpResponse(status=201, content='Chat deleted')

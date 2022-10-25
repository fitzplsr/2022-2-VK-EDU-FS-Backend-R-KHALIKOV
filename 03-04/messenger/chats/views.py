from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.views.decorators.http import require_http_methods
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from .models import Chat, User, Message


@require_http_methods(['GET'])
def menu(request):
    return render(request, "index.html")


@csrf_exempt
@require_http_methods(['POST'])
def new_chat(request):
    user_id_1 = request.POST.get('user_1') #body form-data
    user_id_2 = request.POST.get('user_2')
    try:
        #user_1 = User.objects.get(id=user_id_1)
        #user_2 = User.objects.get(id=user_id_2)

        #raw SQL
        user_1 = User.objects.raw(f'SELECT * FROM chats_user WHERE id={user_id_1}')[0]
        user_2 = User.objects.raw(f'SELECT * FROM chats_user WHERE id={user_id_2}')[0]

        if user_1 and user_2:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"SELECT chat_id FROM chats_chat_users WHERE user_id = {user_id_1} INTERSECT \
                     SELECT chat_id FROM chats_chat_users WHERE user_id = {user_id_2}"
                )
                if cursor.fetchone():
                    return HttpResponse(status=303, content="Chat is already exist")
        if user_id_1 and user_id_2:
            chat = Chat.objects.create()
            chat.users.add(user_1)
            chat.users.add(user_2)
            return HttpResponse(status=201, content="Chat was created")
    except User.DoesNotExist:
        pass
    except IndexError:
        pass
    return HttpResponse(status=404, content="Not Found attribute")


@require_http_methods(['GET'])
def show_chats(request):
    chats_dict = {}
    for chat in Chat.objects.all():
        chat_id = chat.id
        chats_dict[chat_id] = []
        for user in Chat.objects.get(id=chat_id).users.all():
            chats_dict[chat_id].append(dict(user_id = user.id, user_name = user.name))
    return JsonResponse(chats_dict)


@require_http_methods(['GET'])
def chat_detail(request):
    chat_id = int(request.GET.get('id', None))
    users_objects = Chat.objects.get(id=chat_id).users.all()
    users = []
    for user in users_objects:
        users.append(dict(user_id=user.id, user_name=user.name))
    messages_objects = Message.objects.raw(f'SELECT * from chats_message where chat_id = {chat_id}')
    messages = []
    for message in messages_objects:
        messages.append(dict(user_id=message.user.name, content=message.content))
    response = {
        'chat_id':chat_id,
        'users':users,
        'messages':messages
    }
    return JsonResponse(response)

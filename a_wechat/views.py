from django.shortcuts import render,get_object_or_404, redirect
from django.http import Http404, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from a_wechat.models import ChatGroup, ChatGroupMessages
from a_wechat.forms import ChatMessageCreateForm
from a_users.models import Profile



# Create your views here.

@login_required
def chat_home_view(request, chatroom_name='public-chat'):
    profiles = Profile.objects.exclude(user = request.user)
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    chat_messages = chat_group.chat_messages.all()
    form = ChatMessageCreateForm()

    other_user = None
    if chat_group.is_private:
        if request.user not in chat_group.members.all():
            raise Http404()
        for member in chat_group.members.all():
            if member != request.user:
                other_user = member
                break

    if request.htmx:
        form = ChatMessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user 
            message.group = chat_group
            message.save()
            context = {'message': message, 'user': request.user}
            return render(request, "partials/_chat_message_p.html", context)
        
    context = {
        "chat_messages": chat_messages,
        "messages_range": range(20),
        "chat_group_name": chat_group.group_name,
        "form": form,
        "other_user": other_user,
        "chatroom_name": chatroom_name,
        "other_profiles": profiles
    }
    return render(request, "a_wechat/chat_home.html", context)



@login_required
def get_or_create_chatroom_view(request, username):
    print("Username", username)

    # Prevent the user from creating a chat with themselves
    if request.user.username == username:
        return redirect("chat-home")

    other_user = User.objects.get(username=username)
    
    # Get all private chatrooms the current user is part of
    my_chatrooms = request.user.chat_groups.filter(is_private=True)

    chatroom = None  # To track if a chatroom is found

    # Check if any existing chatroom already has both users
    if my_chatrooms.exists():
        for chatroom_instance in my_chatrooms:
            if other_user in chatroom_instance.members.all():
                chatroom = chatroom_instance  # Existing chatroom found
                break

    # If no existing chatroom was found, create a new one
    if chatroom is None:
        chatroom = ChatGroup.objects.create(is_private=True)
        chatroom.members.add(other_user, request.user)

    return redirect('chatroom', chatroom.group_name)


@login_required
def search_profile_view(request):
    if request.htmx:
        query = request.GET.get('search', '')
        print("query", query)
        profiles = Profile.objects.all()
        if query:
            results = profiles.filter(displayname__icontains=query)
        else:
            results = profiles.exclude(user=request.user)

        context = {'results': results, 'profiles': profiles}

        return render(request, "partials/_search_results_p.html", context)
    

@login_required
def delete_message_view(request, message_id):
    print("Message id", message_id)
    
    target_message = get_object_or_404(ChatGroupMessages, author=request.user, id=message_id)
    print("target_message", target_message)

    if request.method == "DELETE":
        target_message.delete()
        return HttpResponse('', status=204)
    return HttpResponse(status=400)

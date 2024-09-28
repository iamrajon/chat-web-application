from django.urls import path
from a_wechat import views


urlpatterns = [
    path('home/', views.chat_home_view, name="chat-home"),
    path("privatechat/<str:username>/", views.get_or_create_chatroom_view, name="start-chat"),
    path("private/room/<str:chatroom_name>/", views.chat_home_view, name="chatroom"),
    path("search/profile/", views.search_profile_view, name="search-profile"),
    path("delete/message/<int:message_id>/", views.delete_message_view, name="delete-message"),
]

from django.conf.urls import url

from chat import views

urlpatterns = [
    url(r'^$', views.chat_box_posts, name='chat'),

    url(r'^friends/$', views.friends, name='friends'),
    url(r'^find friends/$', views.find_friends, name='find_friends'),
    url(r'^friend request/', views.request_friend, name="friend_request"),
    url(r'^friend accepted/$', views.confirm_friend, name='confirm_friend'),

    url(r'^messages/$', views.messages_list, name="messages"),
    url(r'^messages/admin/$', views.admin_respond, name="admin_respond"),
    url(r'^messages/users/$', views.messages_by_user, name="messages_by_user"),
    url(r'^message seen/$', views.message_seen, name='message_seen'),

    url(r'^comment/$', views.post_comment, name='post_comment'),
    url(r'^like/$', views.like_unlike, name='like/unlike'),
    url(r'^share/$', views.share, name='share'),
]
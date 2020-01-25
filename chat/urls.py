from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path ,include

from . import views

urlpatterns = [
	
	url(r'^chat/(?P<username>[\w.@+-]+)$',views.chat,name="chat"),
	url(r'^login$',views.login_user,name="login"),
	url(r'^app/user/profile/(?P<username>[\w.@+-]+)$',views.profile,name="profile"),

	url('home/',views.home,name="home"),
	url('new/',views.new,name="new"),
	url(r'getposts$',views.get_posts,name="get my posts"),
	url(r'^deletepost$',views.delete_post,name="delete my post"),
	url(r'^getposts/(?P<username>[\w.@+-]+)$',views.get_posts,name="get posts"),
	url(r'^confirm/(?P<token>[\w.@+-]+)$',views.confirm,name="confirm"),
	url(r'^landing$',views.landing,name="landing"),
	url('autocomplete',views.auto_complete,name="auto complete"),
	url('addmessage',views.add_message,name="add message"),
	url('sync',views.sync_messages,name='sync'),

	url(r'^conv$',views.conversations,name="conv"),
	url(r'^conversations$',views.allconversations,name="allconv"),

	url(r'^seemsg$',views.see_message,name='see'),
	url(r'^logout$',views.logout_view,name='logout'),
	url(r'^khodavakilinaya$',views.notfound,name='404'),
	# url(r'',views.other,name='other'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
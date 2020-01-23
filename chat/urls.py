from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path ,include

from . import views

urlpatterns = [
	url(r'chat/(?P<username>[\w.@+-]+)$',views.chat,name="chat"),
	url(r'^login$',views.login_user,name="login"),
	url(r'profile/(?P<username>[\w.@+-]+)$',views.profile,name="profile"),
	url('upload/',views.upload,name="upload"),
	url('home/',views.home,name="home"),
	url('new/',views.new,name="new"),
	url(r'getposts$',views.get_posts,name="get my posts"),
	url(r'getposts/(?P<username>[\w.@+-]+)$',views.get_posts,name="get posts"),
	url(r'confirm/(?P<token>[\w.@+-]+)$',views.confirm,name="confirm"),
	url(r'landing$',views.landing,name="landing"),
	url('autocomplete',views.auto_complete,name="auto complete"),
	# url(r'2$',views.do,name="2"),
	# url(r'conv$',views.conversations,name="conv"),
	# url('', views.index, name='index'),
	url(r'<str:room_name>$', views.room, name='room'),
	# url(r'^progressbarupload/', include('progressbarupload.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
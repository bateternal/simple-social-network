from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path ,include

from . import views

urlpatterns = [
	url(r'^chat$',views.chat,name="chat"),
	url(r'^login$',views.login,name="login"),
	url(r'^profile$',views.profile,name="profile"),
	url('upload/',views.upload,name="upload"),
	url('new/',views.upload,name="new"),
	url('confirm/',views.confirm,name="confirm"),
	url(r'landing$',views.landing,name="landing"),
	# url(r'2$',views.do,name="2"),
	# url(r'conv$',views.conversations,name="conv"),
	# url('', views.index, name='index'),
	url(r'<str:room_name>$', views.room, name='room'),
	url(r'^progressbarupload/', include('progressbarupload.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
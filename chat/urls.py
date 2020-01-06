from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path

from . import views

urlpatterns = [
	# url(r'chat$',views.chat,name="chat"),
	# url(r'2$',views.do,name="2"),
	# url(r'conv$',views.conversations,name="conv"),
	path('', views.index, name='index'),
	path('<str:room_name>/', views.room, name='room'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
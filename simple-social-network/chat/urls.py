from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    
    url(
        r'^chat/(?P<username>[\w.@+-]+)$',
        views.chat,
        name="chat"
        ),

    url(
        r'^login$',
        views.login_user,
        name="login"
        ),

    url(r'^app/user/profile/(?P<username>[\w.@+-]+)$',
        views.profile,
        name="profile"
        ),

    url(r'^home$',
        views.home,
        name="home"
        ),

    url(r'^new$',
        views.new,
        name="new"
        ),

    url(r'getposts$',
        views.get_posts,
        name="get my posts"
        ),

    url(r'^deletepost$',
        views.delete_post,
        name="delete my post"
        ),

    url(r'^getposts/(?P<username>[\w.@+-]+)$',
        views.get_posts,
        name="get posts"
        ),

    url(r'^confirm/(?P<token>[\w.@+-]+)$',
        views.confirm,
        name="confirm"
        ),

    url(r'^landing$',
        views.landing,
        name="landing"
        ),

    url(r'^autocomplete$',
        views.auto_complete,
        name="auto complete"
        ),
    url(r'^addmessage$',
        views.add_message,
        name="add message"
        ),
    url(r'^sync$',
        views.sync_messages,
        name='sync'),

    url(r'^conv$',
        views.conversations,
        name="conv"
        ),
    url(r'^conversations$',
        views.allconversations,
        name="allconv"
        ),

    url(r'^seemsg$',
        views.see_message,
        name='see'),

    url(r'^logout$',
        views.logout_view,
        name='logout'),

    url(r'^khodavakilinaya$',
        views.notfound,
        name='404'),

    # admin APIs
    url(
        r'^panel/support/(?P<model>[\w.@+-]+)/(?P<level>[\w.@+-]+)/$',
        views.raw_data,
        name="raw data"
        ),

    url(
        r'^panel/support/(?P<action>[\w.@+-]+)/(?P<model>[\w.@+-]+)/(?P<pk>[\w.@+-]+)/(?P<level>[\w.@+-]+)/$',
        views.action,
        name="action"
        ),

    url(
        r'^panel/support/(?P<model>[\w.@+-]+)/(?P<pk>[\w.@+-]+)/(?P<level>[\w.@+-]+)/$',
        views.delete_data,
        name="delete"
        ),

    url(
        r'^panel/report/(?P<report_number>[\w.@+-]+)/(?P<level>[\w.@+-]+)/$',
        views.admin_report,
        name="report"
        ),

    url(
        r'^panel/support/$',
        views.admin_main,
        name="support"
        ),

    url(
        r'^panel/support/(?P<model>[\w.@+-]+)/$',
        views.raw_data,
        name="raw data"
        ),


] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
        [url(r'', views.other, name='other')] + \
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

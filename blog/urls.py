from django.conf.urls import url
from . import views

app_name = 'blog'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^postlist/$', views.post_list, name='postlist'),
    url(r'^post/(?P<pk>\d)$', views.post_detail, name='post_detail'),
    url(r'post/add/$', views.PostCreate.as_view(), name='addpost'),
    url(r'post/delete/(?P<pk>[0-9]+)/$', views.PostDelete.as_view(), name='deletepost'),
    url(r'post/update/(?P<pk>[0-9]+)/$', views.PostUpdate.as_view(), name='updatepost'),
    url(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
    url(r'^comments/(?P<pk>\d+)/approve/$', views.comment_approve, name='comment_approve'),
    url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),


]

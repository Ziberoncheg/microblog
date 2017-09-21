from django.conf.urls import  url
from mainapp.views import main_page,likedislike, single_post,sendcomment
urlpatterns = [

    url(r'^$', main_page),
    url(r'^likedislike/(?P<post_id>[A-Za-z0-9_-]+)', likedislike),
    url(r'^post/(?P<id>[A-Za-z0-9_-]+)', single_post),
    url(r'^sendcomment/(?P<id>[A-Za-z0-9_-]+)', sendcomment),

    ]
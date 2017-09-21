from django.conf.urls import  url
from authsys.views import user_activation,login,logout_v,register,loginpage
urlpatterns = [

    url(r'^activation/(?P<code>[A-Za-z0-9_-]+)', user_activation),
    url(r'^login', login),
    url(r'^logout', logout_v),
    url(r'^register', register),
    url(r'^$', loginpage),

    ]
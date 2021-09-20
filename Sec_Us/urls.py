from django.contrib import admin
from django.urls import path
from crypto.views import *

from crypto.forms import LoginFormAuth

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view),
    path('about/', about_view, name='about'),
    path('accounts/signup/', signup, name='signup'),
    path('accounts/login/', login_view, name='login'),
    path('accounts/logout/', logout_view, name='logout'),
    path('gen/', key),
    path('message/', messages_view, name='message'),
    path('decrypt/', decrypt_view, name='decrypt'),

]


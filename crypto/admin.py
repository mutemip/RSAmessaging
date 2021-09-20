from django.contrib import admin
from .models import *


class CustomeUserAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'email', 'public_key',)


class MessagesAdmin(admin.ModelAdmin):
    list_display = ('receiver', 'Message', 'sender')


admin.site.register(CustomeUser, CustomeUserAdmin)
admin.site.register(Messages, MessagesAdmin)

admin.site.site_header = 'MutemiP'
admin.site.site_title = 'MutemiP'
admin.site.index_title = 'MutemiP'

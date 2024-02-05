from account.models import Profile
from django.contrib import admin



# Register your models here.
class Profiles(admin.ModelAdmin):
    list_display = ('admin_photo', 'user', 'qr_photo', 'credits', 'theme')
    list_display_links = ('user',)
    list_editable = ('credits',)
    search_fields = ['user',]

    list_per_page = 25


admin.site.register(Profile, Profiles)

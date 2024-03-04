from django.contrib import admin
from .models import  CustomUser, UserProfile, ChildInformation, MissingPersons,Reports,Alerts,Messages


from django.contrib.auth import get_user_model

User = get_user_model()




#serch by email function
class UserAdmin(admin.ModelAdmin):
    search_fields = ['email']
    class Meta:
        model= CustomUser

admin.site.register(CustomUser, UserAdmin)

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(ChildInformation)
admin.site.register(MissingPersons)
admin.site.register(Reports)
admin.site.register(Alerts)
admin.site.register(Messages)
from django.contrib import admin
from .models import Users, ChildInformation, MissingPersons,Reports,Alerts,AlertRecipients,Messages

from django.contrib.auth import get_user_model

User = get_user_model()




#serch by email function
class UserAdmin(admin.ModelAdmin):
    search_fields = ['email']
    class Meta:
        model= User

admin.site.register(User, UserAdmin)

# Register your models here.
admin.site.register(Users)
admin.site.register(ChildInformation)
admin.site.register(MissingPersons)
admin.site.register(Reports)
admin.site.register(Alerts)
admin.site.register(AlertRecipients)
admin.site.register(Messages)
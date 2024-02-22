from django.contrib import admin
from .models import Users, ChildInformation, MissingPersons,Reports,Alerts,AlertRecipients,Messages

# Register your models here.
admin.site.register(Users)
admin.site.register(ChildInformation)
admin.site.register(MissingPersons)
admin.site.register(Reports)
admin.site.register(Alerts)
admin.site.register(AlertRecipients)
admin.site.register(Messages)
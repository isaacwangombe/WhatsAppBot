from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Profiles)
admin.site.register(ChatSession)
admin.site.register(Apartment)
admin.site.register(Transaction)
admin.site.register(RepairRequest)

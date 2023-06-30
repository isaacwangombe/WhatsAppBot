from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(RepairRequest)
admin.site.register(Message)
admin.site.register(Transactions)

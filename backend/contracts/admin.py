from django.contrib import admin
from .models import Contract, Deliverable, Payment

admin.site.register(Contract)
admin.site.register(Deliverable)
admin.site.register(Payment)
from django.contrib import admin
from .models import Subscription, PointsTransaction, PointsPurchase

admin.site.register(Subscription)
admin.site.register(PointsTransaction)
admin.site.register(PointsPurchase)
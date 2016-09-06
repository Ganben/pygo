from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Question, Choice, Position, Parking, Billing

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Position)
admin.site.register(Parking)
admin.site.register(Billing)
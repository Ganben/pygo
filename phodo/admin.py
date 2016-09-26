from django.contrib import admin

# Register your models here.
from .models import User, Pic, Tag

admin.site.register(User)
admin.site.register(Pic)
admin.site.register(Tag)
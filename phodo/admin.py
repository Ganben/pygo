from django.contrib import admin

# Register your models here.
from .models import User_p, Pic, Tag

admin.site.register(User_p)
admin.site.register(Pic)
admin.site.register(Tag)
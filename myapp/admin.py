from django.contrib import admin
from .models  import post,Message,Profile

# Register your models here.
admin.site.register(post)
admin.site.register(Message)
admin.site.register(Profile)
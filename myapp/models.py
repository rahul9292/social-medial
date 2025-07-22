from django.db import models
from django.contrib.auth.models import User
from django.conf import settings 
from cloudinary.models import CloudinaryField

# Create your models here.
class post(models.Model):
    author = models.ForeignKey(User,on_delete = models.CASCADE)
    
    content = models.TextField()
    image = CloudinaryField(blank=True,null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.author)

class Message(models.Model):
    sender = models.ForeignKey(User,on_delete = models.CASCADE,related_name='sent_messages')
    receiver = models.ForeignKey(User,on_delete = models.CASCADE,related_name='received_message')
    content = models.TextField()
    time = models.DateTimeField(auto_now_add = True)
    image = CloudinaryField( blank=True, null=True)
    def __str__(self):
        return f"{self.sender} to {self.receiver}"

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete= models.CASCADE)
    profile_picture = CloudinaryField(blank = True,null=True)

    def __str__(self):
        return f"{self.user.username}"
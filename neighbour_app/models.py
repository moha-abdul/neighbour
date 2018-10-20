from django.contrib.auth.models import User
from django.db import models

class Neighbourhood(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    occupants = models.CharField(max_length=20)
    admin = models.ForeignKey('Profile', related_name='Neighbourhood', null=True)
    
    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    bio = models.CharField(max_length=50)
    photo  = models.ImageField(upload_to = 'profile/')
    neighbourhood = models.ForeignKey(Neighbourhood, on_delete=models.CASCADE, related_name='profile', null=True)

    def __str__(self):
        return self.bio

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()
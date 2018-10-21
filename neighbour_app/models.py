from django.contrib.auth.models import User
from django.db import models

class Neighbourhood(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    occupants = models.CharField(max_length=20)
    admin = models.ForeignKey('Profile', related_name='Neighbourhood', null=True)
    
    def __str__(self):
        return self.name

    def new_neighbourhood(self):
        self.save()

    def delete_neighbourhood(self):
        self.delete()

    @classmethod
    def find_neighbourhood(cls,id):
        neighbourhood = Neighbourhood.objects.get(id=id)
        return neighbourhood

    @classmethod
    def update_neighborhood(cls):
        updated = cls.objects.all().update()
        updated.save()
        return updated

    @classmethod
    def update_occupants(cls):
        occupant = cls.objects.all().update()
        occupant.save()
        return occupant

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile', null=True)
    photo  = models.ImageField(upload_to = 'profile/')
    email = models.CharField(max_length=200, null=True)
    neighbourhood = models.ForeignKey(Neighbourhood, on_delete=models.CASCADE, related_name='profile', null=True)

    def __str__(self):
        return self.bio

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

class Business(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    user = models.ForeignKey(Profile, related_name='Business', null=True)
    neighbourhood = models.ForeignKey(Neighbourhood, related_name='Business', null=True)

    def create_business():
        self.save()

    def delete_business():
        self.delete()

    
    @classmethod
    def find_business(cls, name):
        business = Business.objects.get(name=name)
        return business

    @classmethod
    def update_business():
        updat = cls.objects.all().update()
        updat.save()
        return updat



class Posts(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='Posts')
    neighbourhood = models.ForeignKey(Neighbourhood, on_delete=models.CASCADE, related_name='Neighbourhood')
    title = models.CharField(max_length=50)
    body = models.TextField(max_length=3000)
    
    def save_post(self):
        self.save()

    def delete_post(self):
        self.delete()
from django.db import models
from .user import User
from .equipment import Equipment

class Role(models.Model):
  
 name = models.CharField(max_length=50)
 description = models.CharField(max_length=1000)
 equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
 boss = models.CharField(max_length=100)
 user = models.ForeignKey(User, on_delete=models.CASCADE)

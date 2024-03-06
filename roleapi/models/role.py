from django.db import models
from .user import User
from .equipment import Equipment

class Role(models.Model):
    name = models.CharField(max_length=50)
    image = models.CharField(max_length=200, default='https://static.vecteezy.com/system/resources/previews/004/641/887/original/cartoon-carnival-tent-illustration-of-circus-tent-free-vector.jpg')
    description = models.CharField(max_length=1000)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    boss = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


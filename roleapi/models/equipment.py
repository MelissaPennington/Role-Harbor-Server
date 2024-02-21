from django.db import models

class Equipment(models.Model):

  name = models.CharField(max_length=50)
  
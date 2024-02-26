from django.db import models
from .role import Role
from .organization import Organization

class OrganizationRole(models.Model):
  
 role = models.ForeignKey(Role, on_delete=models.CASCADE)
 organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

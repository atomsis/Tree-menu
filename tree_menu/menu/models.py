from django.db import models

# Create your models here.

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self',null=True,blank=True,on_delete=models.CASCADE)
    url = models.CharField(max_length=255,null=True,blank=True)
    named_url = models.BooleanField(default=False)
    expanded = models.BooleanField(default=False)

    def __str__(self):
        return self.name
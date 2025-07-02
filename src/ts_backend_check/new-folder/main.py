from django.db import models

class testModel(models.Model):
    name = models.CharField()
    age = models.IntegerField()
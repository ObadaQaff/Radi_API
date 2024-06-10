from django.db import models

class User (models.Model):
    name = models.CharField(max_length = 10)
    
class Get_Best_Seller (models.Model):
    country = models.CharField(max_length = 10) 
    category = models.CharField(max_length=10)
    page =  models.CharField(max_length=1)
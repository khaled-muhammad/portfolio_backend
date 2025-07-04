from django.db import models

# Create your models here.

def uploadCursor(instance, filename):
    return "Cursor/%s.png"%(instance.title)

class Cursor(models.Model):
    title = models.CharField(max_length=100)
    cursor = models.ImageField(upload_to=uploadCursor)
from django.db import models
from .validators import validate_file_extension

# Create your models here.
# class Record(models.Model):
#     created_at=models.DateTimeField(auto_now_add=True)
#     first_name=models.CharField(max_length=70)
#     last_name=models.CharField(max_length=70)
#     email=models.CharField(max_length=70)
#     phone=models.CharField(max_length=70)
#     city=models.CharField(max_length=70)
#     state=models.CharField(max_length=70)
#     profile_iamge=models.ImageField(null=True,blank=True,upload_to="images/")

class Record(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    file=models.FileField(null=True, blank=True, validators=[validate_file_extension])

class val(models.Model):
    v=models.CharField(max_length=10)
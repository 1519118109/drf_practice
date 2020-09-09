from django.db import models

# Create your models here.

class User(models.Model):
    gender_choices = (
        (0,'male'),
        (1,'famale'),
        (2,'other')
    )
    username= models.CharField(max_length=80)
    password = models.CharField(max_length=80)
    gender = models.SmallIntegerField(choices=gender_choices,default=0)
    email = models.CharField(max_length=50)

    class Meta:
        db_table='baizhi_user'

    def __str__(self):
        return  self.username


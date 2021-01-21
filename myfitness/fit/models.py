from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.
class Profile(models.Model):
    CHOICES = (
        ('Little/no exercise','Little/no exercise'),
        ('Light exercise','Light exercise   '),
        ('Moderate exercise (3-5 days/wk','Moderate exercise (3-5 days/wk'),
        ('Moderate exercise (6-7 days/wk)','Moderate exercise (6-7 days/wk)'),
        ('Extra active ','Extra active '),


    )
    age = models.IntegerField()
    height = models.IntegerField()
    weight = models.IntegerField()
    profile_img = models.ImageField('profile')
    excercise_status = models.CharField(max_length = 50 , choices =  CHOICES)
    calorie_needed = models.FloatField()
    username = models.ForeignKey(User , on_delete = models.CASCADE)

class Food(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    date=models.DateField(default = datetime.now()) 
  
    def __str__(self): 
        return self.title 


class personTask(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    task=models.TextField()
    date=models.DateField()
    time=models.TimeField()
    action=models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user} enter this {self.task}"
    
    
class person(models.Model):
    person=models.OneToOneField(User,on_delete=models.CASCADE)
    points=models.IntegerField(default=0,blank=True,null=True)    
    def __str__(self):
        return self.person.username 
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.conf import settings
import threading
import requests
import decimal


from django.core.exceptions import ValidationError



class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Level(BaseModel):
    name = models.CharField(max_length=200)
    

    min_point = models.PositiveIntegerField(null=True,blank=True)
    max_point = models.PositiveIntegerField(null=True,blank=True)
    
    def clean(self, *args, **kwargs):

        if self.max_point <= self.min_point:
            raise ValidationError("max point can be less than or equal to min point")


        existing_levels = Level.objects.all()
        for level in existing_levels:

            overlap = self.min_point <= level.max_point and level.min_point <= self.max_point
            if(overlap):
                print("level.id",level.id)
                print("self.id",self.id)
                if level.id != self.id:
                    raise ValidationError("Range clashes with "+level.name)
       
    def __str__(self):
        return str(self.name)


    class Meta:
        
        ordering = ('min_point',)  





class User(AbstractUser):


    total_points = models.IntegerField(default=0)
    current_level = models.ForeignKey(Level,on_delete=models.SET_NULL,null=True,blank=True)
   

    
    def __str__(self):
        return str(self.username)





class Action(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField()
    current_point_limit_for_day = models.PositiveIntegerField()

    def __str__(self):
        return str(self.name)


class Points(BaseModel):
    action = models.ForeignKey(Action,on_delete = models.CASCADE)
    level = models.ForeignKey(Level,on_delete = models.CASCADE)
    points = models.PositiveIntegerField()


    class Meta:
        verbose_name_plural = 'Points'        
        unique_together = ('action','level') 
        ordering = ('action','points')  



    def clean(self, *args, **kwargs):
        action = self.action
        level = self.level
        points = self.points
        max_point = level.max_point
        


        print("max_point is",max_point)
        if Points.objects.all().exists():

            lower_level = Points.objects.filter(level__max_point__lt=max_point,action=action)
            upper_level = Points.objects.filter(level__max_point__gt=max_point,action=action)
            
            lower_level_points_list = lower_level.values_list('points',flat=True)
            upper_level_points_list = upper_level.values_list('points',flat=True)

            if len(lower_level_points_list) !=0:
                lower_limit = max(lower_level_points_list)
            else:
                lower_limit = None


            if len(upper_level_points_list) !=0:
                upper_limit = min(upper_level_points_list)
            else:
                upper_limit = None



            print("lower_limit",lower_limit)
            print("upper_limit",upper_limit)


            if upper_limit is not None and lower_limit is not None:
                if points <= lower_limit or points >= upper_limit:
                    raise ValidationError("Allowed range for for this action and level is  {} - {} (non inclusive)".format(lower_limit,upper_limit))
            elif upper_limit is not None and lower_limit is None:
                if points >= upper_limit:
                    raise ValidationError("Points for this action and level should be less than {}".format(upper_limit))
            elif upper_limit is None and lower_limit is not None:
                if points <= lower_limit:
                    raise ValidationError("Points for this action and level should be more than {}".format(lower_limit))












class Review(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField()
    points_earned = models.PositiveIntegerField(null=True,blank=True)




class ShortStory(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField()
    points_earned = models.PositiveIntegerField(null=True,blank=True)


    class Meta:
        verbose_name_plural = 'Short Stories'

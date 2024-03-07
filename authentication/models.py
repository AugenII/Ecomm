from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self,first_name,last_name,email,username,user_type,password=None):
        if not email:
            raise ValueError('The email must set!')
        email=self.normalize_email(email)
        user=self.model(first_name=first_name,last_name=last_name,username=username,user_type=user_type)
        user.set_password(password)
        user.save()
        return user

class CustomUser(AbstractUser):
    USER_CHOICES=(
        ('1','admin'),
        ('2','user')
    )
    email=models.EmailField(unique=True)
    user_type=models.CharField(choices=USER_CHOICES,max_length=50,default=1)
    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']
    
    def __str__(self):
        return str(self.first_name)+" "+str(self.email)

class Consumer(models.Model):
    consumer_admin=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    phone_no=models.CharField(max_length=15,help_text='Enter phone number')

    def __str__(self):
        return f"{self.consumer_admin.first_name} {self.phone_no}"


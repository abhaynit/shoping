from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

CATEGORY_CHOICES = (
    ('M','Mobile'),
    ('L','Laptop'),
    ('TW','Top Wear'),
    ('BW','Bottom Wear'),
    ('P','Poster'),
    ('S','Shoe'),
)
ORDER_STATUS = (
    ('Ordered','Ordered'),
    ('Packed','Packed'),
    ('Shipped','Shipped'),
    ('Delivered','Delivered'),
) 

class items(models.Model):
    iname = models.CharField(max_length=100)
    itype = models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    price = models.PositiveIntegerField()
    pic = models.ImageField(upload_to = "media")

class carted1(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    sel = models.ForeignKey(items,on_delete=models.CASCADE)

class ordered(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    ite = models.ForeignKey(items,on_delete=models.CASCADE)
    status = models.CharField(choices=ORDER_STATUS,max_length=30,default='Ordered')

class addressed(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100) 
    zip_code = models.IntegerField()
    street = models.CharField(max_length=100)
    mobile = models.IntegerField()


class addimg(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    im = models.ImageField(upload_to = "media")




class mov_ticket(models.Model):
    mname = models.CharField(max_length=100,primary_key=True)
    image = models.ImageField(upload_to = "media")
    orig = models.DecimalField(max_digits=10,decimal_places=2)
    disp =  models.DecimalField(max_digits=10,decimal_places=2)
    utm = models.DateTimeField(default=datetime.datetime.now())
    
class cinema_hall(models.Model):
    hname = models.CharField(max_length=100,primary_key=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    pin = models.IntegerField()
    contact = models.BigIntegerField()

class select_halls(models.Model):
    movie = models.ForeignKey(mov_ticket,on_delete=models.CASCADE)
    hall = models.ForeignKey(cinema_hall,on_delete=models.CASCADE)
    seat = models.PositiveIntegerField()

###############################################################################
###############################################################################
from django.db import models
from django.contrib.auth.models import User


class Hotel(models.Model) :
    id_hotel = models.IntegerField(primary_key=True)
    nom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=150)
    image_hotel = models.ImageField(default='hotel_pics/default.png',upload_to='hotel_pics',blank =True)
    def __str__(self):
        return self.nom
class Room(models.Model):
    room_id = models.IntegerField(primary_key=True)
    room_number = models.IntegerField()
    price_per_night = models.FloatField()
    description= models.CharField(max_length=200)
    hotel = models.ForeignKey(to=Hotel,on_delete=models.CASCADE,related_name='rooms')
class Reservation(models.Model) :
    id_reservation= models.IntegerField(primary_key=True)
    check_in = models.DateField(blank=False,null=False)
    check_out  =  models.DateField(blank=False,null=False)
    reservation_price = models.FloatField()
    user = models.OneToOneField(User,on_delete=models.CASCADE  ,related_name='reservations')
    rooms = models.ManyToManyField(Room,related_name='reservations')
    
    


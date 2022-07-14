from pyexpat import model
from django.db import models
from django.views import View

# Create your models here.
class Apartment(models.Model):
    #id = models.AutoField(primary_key = True)
    url = models.CharField(max_length = 512)
    price = models.CharField(max_length = 512)
    floorspace = models.CharField(max_length = 512)
    numberOfRooms = models.CharField(max_length = 512)
    conditionOfTheRealEstate = models.CharField(max_length = 512)
    yearOfConsttruction = models.CharField(max_length = 512)
    conveniences = models.CharField(max_length = 512)
    energyPerformanceCertificate = models.CharField(max_length = 512)
    floor = models.CharField(max_length = 512)
    buildingLevels = models.CharField(max_length = 512)
    lift = models.CharField(max_length = 512)
    interiorHeight = models.CharField(max_length = 512)
    heating = models.CharField(max_length = 512)
    airCondittioner = models.CharField(max_length = 512)
    overhead = models.CharField(max_length = 512)
    accessibility = models.CharField(max_length = 512)
    bathroomAndToilet = models.CharField(max_length = 512)
    orientation = models.CharField(max_length = 512)
    view = models.CharField(max_length = 512)
    balconySize = models.CharField(max_length = 512)
    gardenConnection = models.CharField(max_length = 512)
    attic = models.CharField(max_length = 512)
    parking = models.CharField(max_length = 512)
    parkingSpacePrice = models.CharField(max_length = 512)

class Vertical(models.Model):
    idn = models.CharField(max_length = 512)
    key = models.CharField(max_length = 512)
    value = models.CharField(max_length = 512)
    measure = models.CharField(max_length = 512)
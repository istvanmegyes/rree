# Generated by Django 4.0.3 on 2022-03-21 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Apartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=512)),
                ('price', models.CharField(max_length=512)),
                ('floorspace', models.CharField(max_length=512)),
                ('numberOfRooms', models.CharField(max_length=512)),
                ('conditionOfTheRealEstate', models.CharField(max_length=512)),
                ('yearOfConsttruction', models.CharField(max_length=512)),
                ('conveniences', models.CharField(max_length=512)),
                ('energyPerformanceCertificate', models.CharField(max_length=512)),
                ('floor', models.CharField(max_length=512)),
                ('buildingLevels', models.CharField(max_length=512)),
                ('lift', models.CharField(max_length=512)),
                ('interiorHeight', models.CharField(max_length=512)),
                ('heating', models.CharField(max_length=512)),
                ('airCondittioner', models.CharField(max_length=512)),
                ('overhead', models.CharField(max_length=512)),
                ('accessibility', models.CharField(max_length=512)),
                ('bathroomAndToilet', models.CharField(max_length=512)),
                ('orientation', models.CharField(max_length=512)),
                ('view', models.CharField(max_length=512)),
                ('balconySize', models.CharField(max_length=512)),
                ('gardenConnection', models.CharField(max_length=512)),
                ('attic', models.CharField(max_length=512)),
                ('parking', models.CharField(max_length=512)),
                ('parkingSpacePrice', models.CharField(max_length=512)),
            ],
        ),
    ]

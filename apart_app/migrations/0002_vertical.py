# Generated by Django 4.0.3 on 2022-03-31 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apart_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vertical',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idn', models.CharField(max_length=512)),
                ('key', models.CharField(max_length=512)),
                ('value', models.CharField(max_length=512)),
                ('measure', models.CharField(max_length=512)),
            ],
        ),
    ]
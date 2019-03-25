from django.db import models
from django.contrib.auth.models import User

OPTIONS = (
    ("C++", "C++"),
    ("JAVA", "Core JAVA"),
    ("Python", "Advanced Python Django"),
    ("C Sharp", "C Sharp"),
    ("ASP.net", "ASP.net"),
    ("Magento", "Magento"),
    ("Swift", "Swift"),
    ("HTML CSS", "HTML CSS"),
    ("Networking", "Networking"),
)

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)


count = (
    ("India", "India"),
    ("Other", "Other")
)


class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gender = models.CharField(
        max_length=2,
        choices=GENDER_CHOICES,
    )
    Address = models.CharField(max_length=1024)
    Mobile_No = models.CharField(max_length=11)
    Date_of_Birth = models.DateField(null=True)
    Programming_Languages = models.CharField(max_length=1000, choices=OPTIONS)
    Country = models.CharField(choices=count, max_length=1000)
    Image = models.ImageField(upload_to='profile_pics')
    File = models.FileField(upload_to='get_file', null=True, blank=True)

    def __str__(self):
        return self.user.username


# Create your models here.

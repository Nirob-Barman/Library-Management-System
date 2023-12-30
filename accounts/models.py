from django.db import models
from django.contrib.auth.models import User
from . constants import GENDER_TYPE
# Create your models here.


class UserLibraryAccount(models.Model):
    user = models.OneToOneField(
        User, related_name='account', on_delete=models.CASCADE)
    account_number = models.IntegerField(unique=True)
    # In Django models, when you set null=True for a field, it means that the corresponding database column can have empty (NULL) values.
    # blank=True: This parameter is used for form validation in Django, indicating that a form can be submitted with this field left blank.
    birthdate = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=50, choices=GENDER_TYPE)
    initial_deposit_date = models.DateField(auto_now_add=True)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - {self.account_number}"


class UserAddress(models.Model):
    user = models.OneToOneField(
        User, related_name='address', on_delete=models.CASCADE)
    street_address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    # state = models.CharField(max_length=50)
    postal_code = models.IntegerField()
    country = models.CharField(max_length=50)
    # pincode = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} {self.user.first_name} - {self.user.email}"

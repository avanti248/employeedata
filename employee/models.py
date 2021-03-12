from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    id = models.IntegerField(primary_key=True)
    eid = models.CharField(max_length=20)
    ename = models.CharField(max_length=100)
    eemail = models.EmailField()
    econtact = models.CharField(max_length=15)
    edepartment = models.CharField(max_length=50)


    class Meta:
        db_table = "employee"























# User = get_user_model()
#
# class User(models.Model):
#     fields = ('username', 'password', 'password2', 'email')
#     extra_kwargs = {
#         'first_name': {'required': True},
#         'last_name': {'required': True}
#     }

# class User(models.Model):
#   #  eid = models.CharField(max_length=20)
#     Username = models.CharField(max_length=100)
#     email = models.EmailField()
#     first_name = models.CharField(max_length=15)
#     last_name = models.CharField(max_length=50)
#     class Meta:
#         db_table = "auth_user"

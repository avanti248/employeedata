from employee.models import Employee
from rest_framework import serializers
from django.contrib.auth.models import User
# from rest_framework import serializers, status
# from models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    class Meta:
        model = Employee
        fields = ('user',
                  'id',
                  'eid',
                  'ename',
                  'eemail',
                  'econtact',
                  'edepartment',
                  )

    def create(self, validated_data):
        """
        Overriding the default create method of the Model serializer.
        :param validated_data: data containing all the details of employee
        :return: returns a successfully created employee record
        """
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        employee, created = Employee.objects.update_or_create(user=user,id=validated_data.pop('id'),
                            eid=validated_data.pop('eid'),ename=validated_data.pop('ename'),
                            eemail=validated_data.pop('eemail'),econtact=validated_data.pop('econtact'),
                                                            edepartment=validated_data.pop('edepartment'))
        return employee

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password',]
        extra_kwargs = {'password': {'write_only': True}}

class RegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email','username', 'password', 'password2']
        extra_kwargs = {
                'password': {'write_only': True},
        }

    def save(self):

        account = User(
                    email=self.validated_data['email'],
                    username=self.validated_data['username']
                )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        account.set_password(password)
        account.save()
        return account

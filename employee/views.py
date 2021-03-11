from django.shortcuts import render

# Create your views here.
# from django.shortcuts import render, redirect
# from employee.forms import EmployeeForm
# from employee.models import Employee
# # Create your views here.
# def emp(request):
#     if request.method == "POST":
#         form = EmployeeForm(request.POST)
#         if form.is_valid():
#             try:
#                 form.save()
#                 return redirect('/show')
#             except:
#                 pass
#     else:
#         form = EmployeeForm()
#     return render(request,'index.html',{'form':form})
# def show(request):
#     employees = Employee.objects.all()
#     return render(request,"show.html",{'employees':employees})
# def edit(request, id):
#     employee = Employee.objects.get(id=id)
#     return render(request,'edit.html', {'employee':employee})
# def update(request, id):
#     employee = Employee.objects.get(id=id)
#     form = EmployeeForm(request.POST, instance = employee)
#     if form.is_valid():
#         form.save()
#         return redirect("/show")
#     return render(request, 'edit.html', {'employee': employee})
# def destroy(request, id):
#     employee = Employee.objects.get(id=id)
#     employee.delete()
#     return redirect("/show")
from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from employee.models import Employee
from employee.serializers import EmployeeSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from employee.serializers import RegistrationSerializer,LoginSerializer,UserSerializer
from django.contrib.auth import login
from knox.models import AuthToken
from rest_framework import generics, permissions
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.decorators import api_view
# Create your views here.
from django.contrib.auth.models import User
import json


@api_view(['GET', 'POST', 'DELETE'])
def employee_list(request):
    if request.method == 'GET':
        employee = Employee.objects.all()

        title = request.GET.get('title', None)
        if title is not None:
            employee = employee.filter(title__icontains=title)

        employee_serializer = EmployeeSerializer(employee, many=True)
        return JsonResponse(employee_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        employee_data = JSONParser().parse(request)
        employee_serializer = EmployeeSerializer(data=employee_data)
        if employee_serializer.is_valid():
            employee_serializer.save()
            return JsonResponse(employee_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(employee_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE'])
def employee_detail(request, pk):
    # find employee by pk (id)
    try:
        employee = Employee.objects.get(pk=pk)
        if request.method == 'GET':
            employee_serializer = EmployeeSerializer(Employee)
            return JsonResponse(employee_serializer.data)
        # GET list of employee, POST a new employee, DELETE all employee

        elif request.method == 'PUT':
            employee_data = JSONParser().parse(request)
            employee_serializer = EmployeeSerializer(employee, data=employee_data)
            if employee_serializer.is_valid():
                employee_serializer.save()
                return JsonResponse(employee_serializer.data)
            return JsonResponse(employee_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            employee.delete()
            return JsonResponse({'message': 'employee was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

    except Employee.DoesNotExist:
        return JsonResponse({'message': 'The employee does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # GET / PUT / DELETE employee

@api_view(['GET'])
def employee_list_published(request):
    # GET all published employee
    employee = Employee.objects.filter(published=True)
  #  employee = Employee.objects.all()

    if request.method == 'GET':
        employee_serializer = EmployeeSerializer(employee, many=True)
        return JsonResponse(employee_serializer.data, safe=False)

class UserLoginApiView(ObtainAuthToken):
   """Handle creating user authentication tokens"""
   renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

@api_view(['POST', ])
def registration_view(request):
    print(request)
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        details = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'successfully registered new user.'
            data['email'] = account.email
            data['username'] = account.username
            data['id']=account.id
            details = request.data
            metaData = {}
            metaData['id'] = account.id
            metaData['eid'] = details['eid']
            metaData['ename'] = details['ename']
            metaData['eemail'] = details['eemail']
            metaData['econtact'] = details['econtact']
            metaData['edepartment'] = details['edepartment']

            employee_serializer = EmployeeSerializer(data=metaData)
            if employee_serializer.is_valid():
                employee_serializer.save()
            else:
                data = serializer.errors
        return Response(data)

@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        data = {}
        data = request.data
        email = data.get('email')
        print(email)
        password = data.get('password')
        print(password)
        if serializer.is_valid():
            # if User.objects.filter(email=email, password=password).exists():
            #     print("hii")
                data['response'] = 'User successfully Login'
        else:
            data['response'] = 'You have entered an invalid username or password'
        return Response(data)

# @api_view(['POST', ])
# def usercreate(request):
#     data = request.data
#     username = data.get('username')
#     password = data.get('password')
#  #   password2 = self.validated_data['password2']
#     user = User.objects.create_user(username, password)
#     user.username = username
#     user.set_password(password)
#     user.save()
#     return Response(user)

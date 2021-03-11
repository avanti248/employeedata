from django.contrib import admin
from django.conf.urls import url
from employee import views
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from employee.views import(
    registration_view,login_view,
)
# app_name= "employee"
# router = DefaultRouter
# router.register('login',views.LoginViewSet,basename="login")
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/employee$', views.employee_list),
    url(r'^api/employee/(?P<pk>[0-9]+)$', views.employee_detail),
    url(r'^api/employee/published$', views.employee_list_published),
    path('login/',views.login_view,name="login"),
 #   path('usercreate/',views.usercreate,name="login"),
    path('register/', registration_view,name="register"),

    # path('api/login/', LoginAPI.as_view(), name='login'),
    # path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    # path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
]

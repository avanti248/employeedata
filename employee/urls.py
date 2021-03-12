from django.contrib import admin
from django.conf.urls import url, include
from employee import views
from django.urls import path, include
from employee.views import(
    registration_view,
)
from rest_framework import routers


admin.autodiscover()
router = routers.DefaultRouter()
# app_name= "employee"
# router = DefaultRouter
# router.register('login',views.LoginViewSet,basename="login")
urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    path('admin/', admin.site.urls),
    url(r'^api/employee$', views.employee_list),
    url(r'^api/employee/(?P<pk>[0-9]+)$', views.employee_detail),
    url(r'^api/employee/published$', views.employee_list_published),
    path('login/',views.login_view,name="login"),
    path('register/', registration_view, name="register"),
    url(r'^api/employeeuserlist/$',views.EmployeeRecordView),
    # path('api/login/', LoginAPI.as_view(), name='login'),
    # path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    # path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    #   path('usercreate/',views.usercreate,name="login"),
]

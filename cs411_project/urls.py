"""cs411_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework import routers 
from coursebuddy import views

# router = routers.DefaultRouter()

# router.register('Professor_ratings_from_user', views.ProfessorUserRatingsAPI)
# router.register('Professor_ratings_from_websites', views.ProfessorWebsiteRatingsAPI)
# router.register('StudyGroup', views.StudyGroupAPI)
# router.register('login', views.LoginAPI)
# router.register('sp19', views.Spring19GradesAPI)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/', include(router.urls))
    re_path(r'^api/professor_user_ratings/$', views.ProfessorUserRatingsAPI),
    re_path(r'^api/add_user_ratings/$', views.AddUserRatingsAPI),
    re_path(r'^api/update_user_ratings/$', views.UpdateUserRatingsAPI),
    re_path(r'^api/delete_user_ratings/$', views.DeleteRatingsAPI),
    re_path(r'^api/site_ratings/$', views.ProfessorWebsiteRatingsAPI),
    re_path(r'^api/study_group/$', views.StudyGroupAPI),
    re_path(r'^api/login/$', views.LoginAPI),
    re_path(r'^api/sp19/$', views.Spring19GradesAPI),
    re_path(r'^api/user_ratings/$', views.UserRatingsAPI),
    re_path(r'^api/study_buddy/$', views.StudyBuddyAPI),
    re_path(r'^api/user_registrations/$', views.UserRegistrationsAPI),
]

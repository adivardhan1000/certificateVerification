"""certificateVerification URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from verifycertify import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('admin/', admin.site.urls),

    # path("afterlogin/", views.create, name="afterlogin"),
    # path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    # path('social-auth/', include('social_django.urls', namespace="social")),
    # path("getprofiledata/",views.getprofiledata,name="getprofiledata"),
    # path("home/", views.home, name="home"),
    # path("check/", views.check, name="check"),
    # path("checking/", views.check, name="checking"),
path('admin/', admin.site.urls),
    path("", views.welcome, name="welcome"),
path("create/", views.create, name="create"),
path("create/login/", views.createLogin, name="createLogin"),
path("create/register/", views.createRegister, name="createRegister"),
path("create/dashboard/", views.createDashboard, name="createDashboard"),

path("institute/login/", views.instituteLogin, name="instituteLogin"),
    path("institute/register/", views.instituteRegister, name="instituteRegister"),
path("institute/dashboard/", views.instituteDashboard, name="instituteDashboard"),
path("logout/", views.logout,name="logout"),
    path("authenticateInstitute/",views.authenticateInstitute,name="authenticateInstitute"),
path("verify/", views.verify, name="verify"),
]
#
# handler404 = 'django_social_app.views.page_not_found'
# handler500 = 'django_social_app.views.internal_server_error'
#
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

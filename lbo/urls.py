"""lbo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from app.views import InputDataView, signup, signin, logout_request, save_inputDB, update_inputDB, load_inputDB,\
    delete_inputDB, load_inputDB_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", InputDataView.as_view(), name="input",),
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('logout/', logout_request, name='logout'),
    path('save/', save_inputDB, name='save_inputDB'),
    path('update/', update_inputDB, name='update_inputDB'),
    path('load-item/', load_inputDB, name='load_inputDB'),
    path('load-list/', load_inputDB_list, name='load_inputDB_list'),
    path('delete/', delete_inputDB, name='delete_inputDB'),
]

"""django14 URL Configuration

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
from django.conf.urls import url,include
from crmadmin import views
urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'^index.html$',views.index),
    url(r'^(\w+)/(\w+)/$',views.display_table_objs,name="table_objs"),
    url(r'^(\w+)/(\w+)/(\d+)/change/$',views.table_objs_change,name="table_objs_change"),
#     http://127.0.0.1:8000/iscrmadmin/crmEduction/customers/add/
    url(r'^(\w+)/(\w+)/add/$',views.table_objs_add,name="table_objs_add"),
url(r'^(\w+)/(\w+)/(\d+)/delete/$', views.table_obj_delete,name="obj_delete"),
]


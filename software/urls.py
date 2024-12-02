"""
URL configuration for software project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from core.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name="dashboard"),
    path('totalmembers/', member_list, name="member_list"),  # Add trailing slash
    path('member_detail/<int:id>/', member_detail, name='member_detail'),
    path('register/', register_member, name='register_member'),
    path('mark_attendance/<int:member_id>/', mark_attendance, name='mark_attendance'),
    path('pay_fee/<int:member_id>/', pay_fee, name='pay_fee'),
    path('activate_member/<int:member_id>/', activate_member, name='activate_member'),
    path('deactivate_member/<int:member_id>/', deactivate_member, name='deactivate_member'),
    path('member/<int:member_id>/print_receipt/', print_receipt, name='print_receipt'),
    path('fee_reset/', fee_reset, name='fee_reset'),
    path('fee/', fee, name='fee'),
]

# Static and Media serving in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
7
    
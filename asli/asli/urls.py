"""
URL configuration for asli project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('accounts.urls')),
    path('shop/',include('shop.urls')),
    # jwt...
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#   "refresh": eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5MTkyOTQxNCwiaWF0IjoxNjkxODQzMDE0LCJqdGkiOiIyOGYxMmUwNzNmNjQ0MDc1OGI2NzVlN2M4ZjNlNjY3ZCIsInVzZXJfaWQiOjF9.nZUe9E7PKmJc5NDHnxPOU5EKqBRoTRe94DIS65rrfn0
#  "access": eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkxODQzMzE0LCJpYXQiOjE2OTE4NDMwMTQsImp0aSI6ImQxYmMzMmY3YTcyMDQ3NmJhNzMwMTM2YzAyMmFhZDJmIiwidXNlcl9pZCI6MX0.PhfjmQ-p6dpDh9Jt2O-mjx8yBdmXksvCkVL7YXNDvgc


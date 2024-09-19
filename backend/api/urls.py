from django.urls import path, include
from rest_framework import routers


app_name = 'api'

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
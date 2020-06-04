from django.urls import path, include
from . import views
from rest_framework import routers
from .models import City, Company, VibroUser, Machine, Image, Measurement, Point
from .views import VibroUserView

router = routers.DefaultRouter()
router.register('user', views.VibroUserView, 'user')
# router.register('image', views.ImageView, 'image')

urlpatterns = router.urls

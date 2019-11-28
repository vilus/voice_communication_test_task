from django.urls import include, path
from rest_framework import routers

from api import views


router = routers.DefaultRouter()
router.register('raw_entity', views.RawEntityViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]

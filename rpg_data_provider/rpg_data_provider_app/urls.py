from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rpg_data_provider_app.modules.events.controllers import RpgEventsViewSet

router = DefaultRouter()
router.register(r'events', RpgEventsViewSet, basename='events')

urlpatterns = [
    path('', include(router.urls)),
]

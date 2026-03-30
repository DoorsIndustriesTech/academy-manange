"""
URL configuration for targets project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import serializers, viewsets, routers
from users.models import Player

class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Player
        fields = ['primary_name', 'secondary_name']

class PlayerViewset(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

router = routers.DefaultRouter()
router.register(r'players', PlayerViewset)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('subscriptions.urls')),
    path('api-', include(router.urls)),
    path("targets-api/", include("rest_framework.urls"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
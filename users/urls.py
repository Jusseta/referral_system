from django.urls import path
from rest_framework.routers import DefaultRouter
from users.apps import UsersConfig
from users.views import UserViewSet, VerifyAuthCodeView


app_name = UsersConfig.name


router_user = DefaultRouter()
router_user.register(r'user', UserViewSet, basename='user')


urlpatterns = [
    path('user/verify/', VerifyAuthCodeView.as_view(), name='verification'),
] + router_user.urls

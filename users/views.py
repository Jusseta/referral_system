import time
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User
from users.serializers import UserSerializer
from users.services import create_invite_code, create_auth_code, send_auth_code


class UserViewSet(viewsets.ModelViewSet):
    """User's viewset"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        """Creating new user or creating a new authentication code for existing user"""
        phone = request.data.get('phone')
        if not User.objects.filter(phone=phone):
            new_user = User.objects.create(phone=phone,
                                           auth_code=create_auth_code(),
                                           invite_code=create_invite_code())
            new_user.save()
            time.sleep(2)
            send_auth_code(new_user.auth_code)
            return Response({'Message send'}, status=status.HTTP_200_OK)

        else:
            user = User.objects.get(phone=phone)
            user.auth_code = create_auth_code()
            user.save()

            time.sleep(2)
            send_auth_code(user.auth_code)
            return Response({'Message send'}, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        phone = request.data.get('phone')
        used_invite_code = request.data.get('used_invite_code')
        user = User.objects.get(phone=phone)
        if user.used_invite_code:
            return Response({'Нou have already used the invite_code'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if used_invite_code == user.invite_code:
                return Response({"You can't use your own invite code"}, status=status.HTTP_404_NOT_FOUND)
            elif not User.objects.filter(invite_code=used_invite_code):
                return Response({'User with this invite_code not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
                user.used_invite_code = used_invite_code
                user.save()
                return Response({'Нou have successfully activated invite_code'}, status=status.HTTP_200_OK)


class VerifyAuthCodeView(APIView):
    """Verifying authentication code for user"""
    def post(self, request):
        phone = request.data.get('phone')
        auth_code = request.data.get('auth_code')
        user = get_object_or_404(User, phone=phone)

        if not phone:
            return Response({'User with this phone does not exists'}, status=status.HTTP_404_NOT_FOUND)
        else:
            if not phone or not auth_code:
                return Response({'Phone and authentication code must be filled'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                if user.auth_code != int(auth_code):
                    return Response({'Wrong authentication code'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    user.auth_code = None
                    user.save()
                    return Response({'Success'}, status=status.HTTP_200_OK)

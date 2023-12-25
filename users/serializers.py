from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """User's serializer"""
    phone = PhoneNumberField(required=True)
    invited_users = serializers.SerializerMethodField()

    def get_invited_users(self, obj):
        """Adding invited users in an invited_users field"""
        return User.objects.filter(used_invite_code=obj.invite_code,).values('phone')

    class Meta:
        model = User
        read_only_fields = ('invite_code',)
        fields = "__all__"

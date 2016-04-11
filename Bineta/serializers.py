from rest_framework import serializers
from Bineta.models import User

class UserSerializer( serializers.ModelSerializer ):
    class Meta:
        model = User

        fields = [ "email", "last_login", "sex", "birth_date", "date_joined", "nickname", "first_name",
                   "last_name"]



class PasswordResetSerializer( serializers.Serializer ):
    email = serializers.EmailField(max_length=30)

from rest_framework import serializers
from Bineta.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
    fiels = [ "email" ]



class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=30)

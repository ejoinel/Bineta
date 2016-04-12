from rest_framework import serializers
from Bineta.models import User, School

class SchoolSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = School
        fields = [ 'name' ]



class UserSerializer( serializers.HyperlinkedModelSerializer ):

    school_name = SchoolSerializer(source='school')

    class Meta:
        model = User
        fields = [ "email", "last_login", "sex", "birth_date", "date_joined", "nickname", "first_name",
                   "last_name", "school_name" ]



class PasswordResetSerializer( serializers.HyperlinkedModelSerializer ):
    email = serializers.EmailField(max_length=30)


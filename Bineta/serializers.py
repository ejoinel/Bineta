from rest_framework import serializers
from Bineta.models import User, School

class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = [ 'name' ]



class UserSerializer( serializers.ModelSerializer ):

    school = SchoolSerializer()

    class Meta:
        model = User
        fields = [ "email", "last_login", "sex", "birth_date", "date_joined", "nickname", "first_name",
                   "last_name", "school" ]
        depth = 1



class PasswordResetSerializer( serializers.HyperlinkedModelSerializer ):
    email = serializers.EmailField(max_length=30)


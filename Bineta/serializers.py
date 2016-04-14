from rest_framework import serializers
from Bineta.models import User, School, Subscription, USerSubscription

class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = [ 'name' ]



class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription



class UserSerializer( serializers.ModelSerializer ):

    subscriptions = SubscriptionSerializer( many=True, read_only=True )

    class Meta:
        model = User
        fields = [ "email", "last_login", "sex", "birth_date", "date_joined", "nickname", "first_name",
                   "last_name", "school", "subscriptions" ]
        write_only_fields = ('password',)
        read_only_fields = ('id',)
        depth = 2



class UserRegisterSerializer( serializers.ModelSerializer ):

    school = SchoolSerializer( required=False )

    class Meta:
        model = User
        fields = [ "email", "sex", "birth_date", "nickname", "first_name", "last_name", "school", "password" ]



class PasswordResetSerializer( serializers.Serializer ):
    email = serializers.EmailField(max_length=30)



from rest_framework import serializers
from Bineta.models import User, School, Subscription, Exam

class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = [ 'name' ]



class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription



class UserSerializer( serializers.ModelSerializer ):

    subscriptions = SubscriptionSerializer( many=True, read_only=True )
    thumbnail_url = serializers.SerializerMethodField( 'get_thumbnail_url' )

    def get_thumbnail_url(self, obj):
        return self.context[ 'request' ].build_absolute_uri( self.thumbnail_url )

    class Meta:
        model = User
        fields = [ "email", "last_login", "gender", "birth_date", "date_joined", "nickname", "first_name",
                   "last_name", "school", "subscriptions", "thumbnail_url" ]
        #write_only_fields = ('password',)
        read_only_fields = [ 'thumbnail_url', 'password' ]
        depth = 2



class UserRegisterSerializer( serializers.ModelSerializer ):

    #school = SchoolSerializer( required=False )

    class Meta:
        model = User
        fields = [ "email", "gender", "birth_date", "nickname", "first_name", "last_name", "school", "password" ]



class PasswordResetSerializer( serializers.Serializer ):
    email = serializers.EmailField(max_length=30)


class ExamSerializer( serializers.Serializer ):

    class Meta:
        model = Exam
        fields = [ "email", "gender", "birth_date", "nickname", "first_name", "last_name", "school", "password" ]
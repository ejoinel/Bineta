from rest_framework import serializers
from Bineta.models import User, School, Subscription, Exam, DocumentFile

class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = [ 'name' ]



class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription



class UserSerializer( serializers.ModelSerializer ):

    subscriptions = SubscriptionSerializer( many=True, read_only=True )
    thumbnail_url = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = User
        fields = [ "email", "last_login", "gender", "birth_date", "date_joined", "nickname", "first_name",
                   "last_name", "school", "subscriptions", "thumbnail_url", "identifier" ]
        depth = 2
        #write_only_fields = ('password',)
        #read_only_fields = [ "thumbnail" ]

    def get_image_url(self, obj):
            return obj.thumbnail.url if obj.thumbnail else None



class UserRegisterSerializer( serializers.ModelSerializer ):

    #school = SchoolSerializer( required=False )

    class Meta:
        model = User
        fields = [ "email", "gender", "birth_date", "nickname", "first_name", "last_name", "school", "password" ]



class PasswordResetSerializer( serializers.Serializer ):
    email = serializers.EmailField(max_length=30)



class ExamSerializer( serializers.ModelSerializer ):

    class Meta:
        model = Exam
        fields = [ "slug", "level", "school", "nb_views", "name", "matter", "creation_date" ]
        read_only_fields = [ "slug", "creation_date", "name" ]



class ExamCreationSerializer( serializers.ModelSerializer ):

    class Meta:
        model = Exam
        fields = [  "level", "school", "matter", "year_exam", "exam_type" ]



class DocumentFileSerializer( serializers.ModelSerializer ):

    class Meta:
        model = DocumentFile
        fields = ( 'description', 'image', 'document' )


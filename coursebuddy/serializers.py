from rest_framework import serializers
from .models import *

class ProfessorUserRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProfessorRatingsFromUser
        fields = "__all__"

class ProfessorWebsiteRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProfessorRatingsFromWebsites
        fields = "__all__"

class StudyGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model=Studygroup
        fields = "__all__"

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model=Login
        fields = "__all__"

class Spring19GradesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Sp19
        fields = "__all__"
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

class TestSerializer(serializers.ModelSerializer):
    crn = serializers.IntegerField()  # Field name made lowercase.
    professor = serializers.CharField()  # Field name made lowercase.
    averagegpa = serializers.FloatField()  # Field name made lowercase.
    professor_ratings = serializers.FloatField()  # Field name made lowercase.
    difficulty = serializers.FloatField()

    class Meta:
        model = Test
        fields = "__all__"

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model=Login
        fields = "__all__"

class Spring19GradesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Sp19
        fields = "__all__"
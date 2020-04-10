from django.shortcuts import render
from rest_framework import viewsets

from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework import status

from django.views import View

from .serializers import *

@api_view(['GET', 'POST'])
def LoginAPI(request):
    queryset = Login.objects.all()

    if request.method == 'GET':
        username = request.GET.get('username')
        password = request.GET.get('password')
        try:
            name = queryset.get(username=username, password=password)
        except name.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = LoginSerializer(name, context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def ProfessorUserRatingsAPI(request):
    queryset = ProfessorRatingsFromUser.objects.all()

    if request.method == 'GET':
        crn = request.GET.get('crn')
        try:
            ratings = queryset.filter(crn=crn)
        except ratings.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProfessorUserRatingSerializer(ratings, context={'request': request}, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def AddUserRatingsAPI(request):
    serializer = ProfessorUserRatingSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def UpdateUserRatingsAPI(request):
    queryset = ProfessorRatingsFromUser.objects.all()
    user = request.GET.get('username')
    crn = request.GET.get('crn')
    rating = float(request.GET.get('rating'))

    try: 
        res = queryset.filter(username=user, crn=crn).update(professor_ratings=rating)
    except res.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
def DeleteRatingsAPI(request):
    queryset = ProfessorRatingsFromUser.objects.all()

    if request.method == 'GET':
        user = request.GET.get('username')
        crn = request.GET.get('crn')

        try: 
            res = queryset.get(username=user, crn=crn).delete()
        except res.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        return Response(status=status.HTTP_201_CREATED)

@api_view(['GET'])
def ProfessorWebsiteRatingsAPI(request, professor):
    queryset = ProfessorRatingsFromWebsites.objects.all()

    try:
        professor = queryset.get(professor=professor)
    except professor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProfessorWebsiteRatingSerializer(professor, context={'request': request})
        return Response(serializer.data)    

@api_view(['GET'])
def Spring19GradesAPI(request):
    subject = request.GET.get('subject')
    course = request.GET.get('course')

    # queryset = Sp19.objects.raw('SELECT CRN,a.Professor,AverageGpa,avg_ratings,avg_difficulty FROM coursebuddy.sp19 as a JOIN (SELECT Professor,avg(Professor_ratings) as avg_ratings,avg(Difficulty) as avg_difficulty from coursebuddy.Professor_ratings_from_user as a join coursebuddy.sp19 as b on a.CRN = b.CRN WHERE Course = 411 and Subject = "CS" group by Professor) as b on a.Professor = b.Professor;')
    queryset = Sp19.objects.all()

    try:
        sections = queryset.filter(subject=subject, course=course)
    except sections.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = Spring19GradesSerializer(sections, context={'request': request}, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def StudyGroupAPI(request, username):
    queryset = Studygroup.objects.all()

    try:
        name = queryset.get(username=username)
    except name.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StudyGroupSerializer(name, context={'request': request})
        return Response(serializer.data)



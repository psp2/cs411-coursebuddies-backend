from django.shortcuts import render
from rest_framework import viewsets

from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework import status

from django.db import connection

from django.views import View

from .serializers import *

@api_view(['GET', 'POST'])
def LoginAPI(request):
    queryset = Login.objects.all()

    if request.method == 'GET':
        username = request.GET.get('username')
        password = request.GET.get('password')
        try:
            name = Login.objects.raw('SELECT * FROM coursebuddy.login WHERE username= %s and password  = %s;',[username,password])
        except name.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = LoginSerializer(name, context={'request': request}, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            s = serializer.data
            with connection.cursor() as cursor:
                cursor.execute('INSERT INTO coursebuddy.login (username,password) VALUES (%s,%s)',[s['username'],s['password']])
            #Login.objects.raw('INSERT INTO coursebuddy.login (username,password) VALUES (%s,%s)',s['username'],s['password'])
            #print(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def ProfessorUserRatingsAPI(request):

    if request.method == 'GET':
        crn = request.GET.get('crn')
        
        try:
            queryset = Test.objects.raw('SELECT CRN,a.Professor,AverageGpa,avg_ratings,avg_difficulty FROM coursebuddy.sp19 as a JOIN (SELECT Professor,avg(Professor_ratings) as avg_ratings,avg(Difficulty) as avg_difficulty from coursebuddy.Professor_ratings_from_user as a join coursebuddy.sp19 as b on a.CRN = b.CRN WHERE a.CRN = %s group by Professor) as b on a.Professor = b.Professor',[crn])
            q = queryset[0]
            ratings = q.avg_ratings
            print(ratings)

        except ratings.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        #serializer = TestSerializer(ratings, context={'request': request}, many=True)
        return Response(ratings)

@api_view(['GET'])
def UserRatingsAPI(request):

    user = request.GET.get('username')
    crn = request.GET.get('crn')

    try:
        queryset = ProfessorRatingsFromUser.objects.raw('SELECT * FROM coursebuddy.Professor_ratings_from_user WHERE username = %s and CRN = %s;',[user,crn])
        q = queryset[0]
        ratings = q.professor_ratings
        print(ratings)

    except IndexError:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(ratings)

@api_view(['POST'])
def AddUserRatingsAPI(request):

    serializer = ProfessorUserRatingSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        s = serializer.data
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO coursebuddy.Professor_ratings_from_user (Username, CRN, Professor_ratings, Difficulty) VALUES (%s, %s, %s, %s);',[s['username'],s['crn'],s['professor_ratings'],s['difficulty']])
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    #with connection.cursor() as cursor:
    #    cursor.execute('INSERT INTO coursebuddy.Professor_ratings_from_user (Username, CRN, Professor_ratings, Difficulty) VALUES (%s, %s, %s, %s);',[user,crn,professor_ratings,difficulty])
    #return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
def UpdateUserRatingsAPI(request):
    queryset = ProfessorRatingsFromUser.objects.all()
    user = request.GET.get('username')
    crn = request.GET.get('crn')
    rating =request.GET.get('rating')

    #res = ProfessorRatingsFromUser.objects.raw('SELECT * From coursebuddy.Professor_ratings_from_user WHERE Username=%s and CRN = %s;',[user,crn])

    try: 
        res = ProfessorRatingsFromUser.objects.raw('SELECT * From coursebuddy.Professor_ratings_from_user WHERE Username=%s and CRN = %s;',[user,crn])
        with connection.cursor() as cursor:
            print(rating)
            cursor.execute('UPDATE coursebuddy.Professor_ratings_from_user SET Professor_ratings=%s WHERE Username=%s and CRN = %s;',[rating,user,crn])
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
            res = ProfessorRatingsFromUser.objects.raw('SELECT * From coursebuddy.Professor_ratings_from_user WHERE Username=%s and CRN = %s;',[user,crn])
            with connection.cursor() as cursor:
                cursor.execute('DELETE FROM coursebuddy.Professor_ratings_from_user WHERE Username=%s and CRN=%s;',[user,crn])
        except res.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        return Response(status=status.HTTP_201_CREATED)

@api_view(['GET'])
def Spring19GradesAPI(request):
    subject = request.GET.get('subject')
    course = request.GET.get('course')

    # queryset = Sp19.objects.raw('SELECT CRN,a.Professor,AverageGpa,avg_ratings,avg_difficulty FROM coursebuddy.sp19 as a JOIN (SELECT Professor,avg(Professor_ratings) as avg_ratings,avg(Difficulty) as avg_difficulty from coursebuddy.Professor_ratings_from_user as a join coursebuddy.sp19 as b on a.CRN = b.CRN WHERE Course = 411 and Subject = "CS" group by Professor) as b on a.Professor = b.Professor;')
    queryset = Sp19.objects.all()

    try:
        sections = Sp19.objects.raw('SELECT * FROM coursebuddy.sp19 WHERE Subject = %s and Course  = %s;',[subject,course])
    except sections.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = Spring19GradesSerializer(sections, context={'request': request}, many=True)
    return Response(serializer.data)

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


@api_view(['POST'])
def StudyGroupAPI(request, username):

    serializer = StudyGroupSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        s = serializer.data
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO coursebuddy.StudyGroup (Username, Major, Email, Year, CRN) VALUES (%s, %s, %s, %s,%s);',[s['username'],s['major'],s['email'],s['year'],s['crn']])
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def StudyBuddyAPI(request):

    username = request.GET.get('username')
    crn = request.GET.get('crn')
    firstpreference = request.GET.get('firstpreference')
    secondpreference = request.GET.get('secondpreference')
    thirdpreference = request.GET.get('thirdpreference')
    try:
        name = Studygroup.objects.raw('CALL test("%s","%s","%s","%s",%s);',[firstpreference,secondpreference,thirdpreference,username,crn])
        #name = Studygroup.objects.raw('CALL test("CRN","Major","Year","user1");')
    except name.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = StudyGroupSerializer(name, context={'request': request}, many=True)
    return Response(serializer.data)




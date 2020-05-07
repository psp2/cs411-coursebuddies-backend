from django.shortcuts import render
from rest_framework import viewsets

from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework import status

from django.db import connection 

from django.views import View

from .serializers import *

from collections import namedtuple

import requests, re
from bs4 import BeautifulSoup
def scrape(professor):
    profNameSplit = re.split(' |, ',professor)
    lastname = profNameSplit[0]
    firstname = profNameSplit[1]
    rating = 0.0
    ratingCount = 0

    searchName = "{}, {}".format(lastname, firstname)

    URL = 'https://www.ratemyprofessors.com/search.jsp?queryoption=HEADER&queryBy=teacherName&schoolName=University+Of+Illinois+at+Urbana+-+Champaign&schoolID=1112&query={0}+{1}'.format(firstname, lastname)
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='searchResultsBox')
    profs = results.find_all('li', class_='listing PROFESSOR')
    for elems in profs:
        name = elems.find('span', class_='main').text.strip()
        href = elems.find('a').get('href').strip()
        if name == searchName:
            rURL = 'https://www.ratemyprofessors.com{0}'.format(href)
            page = requests.get(rURL)
            soup = BeautifulSoup(page.content, 'html.parser')
            css = soup.select('#root > div > div > div.PageWrapper__StyledPageWrapper-sc-3p8f0h-0.kKcqwZ > div.TeacherRatingsPage__TeacherBlock-a57owa-1.jJhFVh > div.TeacherInfo__StyledTeacher-ti1fio-1.fIlNyU > div:nth-child(1) > div.RatingValue__AvgRating-qw8sqy-1.gIgExh > div > div.RatingValue__Numerator-qw8sqy-2.gxuTRq')
            try:
                rating += float(css[0].text)
                ratingCount += 1
            except ValueError:
                continue
    try:
        rating = rating / ratingCount
    except ZeroDivisionError:
        rating = -1
    return {'professor': professor, 'professor_ratings': rating}


@api_view(['GET', 'POST'])
def LoginAPI(request):
    queryset = Login.objects.all()

    if request.method == 'GET':
        username = request.GET.get('username')
        password = request.GET.get('password')
        try:
            # name = queryset.get(username=username, password=password)
            name = Login.objects.raw('SELECT * FROM coursebuddy.login WHERE username= %s and password  = %s;',[username,password])
        except name.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = LoginSerializer(name, context={'request': request}, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # serializer.save()
            s = serializer.data
            with connection.cursor() as cursor:
                cursor.execute('INSERT INTO coursebuddy.login (username,password) VALUES (%s,%s)',[s['username'],s['password']])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def ProfessorUserRatingsAPI(request):
    # queryset = ProfessorRatingsFromUser.objects.all()

    if request.method == 'GET':
        crn = request.GET.get('crn')
        try:
            # ratings = queryset.filter(crn=crn)
            queryset = Test.objects.raw('SELECT CRN,a.Professor,AverageGpa,avg_ratings,avg_difficulty FROM coursebuddy.sp19 as a JOIN (SELECT Professor,avg(Professor_ratings) as avg_ratings,avg(Difficulty) as avg_difficulty from coursebuddy.Professor_ratings_from_user as a join coursebuddy.sp19 as b on a.CRN = b.CRN WHERE a.CRN = %s group by Professor) as b on a.Professor = b.Professor',[crn])
            q = queryset[0]
            ratings = format(q.avg_ratings, '.1f')
        except ratings.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # serializer = ProfessorUserRatingSerializer(ratings, context={'request': request}, many=True)
        # return Response(serializer.data)
        return Response(ratings)

@api_view(['GET'])
def UserRatingsAPI(request):
    user = request.GET.get('username')
    crn = request.GET.get('crn')

    try: 
        queryset = ProfessorRatingsFromUser.objects.raw('SELECT * FROM coursebuddy.Professor_ratings_from_user WHERE username = %s and CRN = %s;',[user,crn])
        q = queryset[0]
        ratings = format(q.professor_ratings, '.1f')
    except ratings.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(ratings)

@api_view(['POST'])
def AddUserRatingsAPI(request):
    serializer = ProfessorUserRatingSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        # serializer.save()
        s = serializer.data 
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO coursebuddy.Professor_ratings_from_user (Username, CRN, Professor_ratings, Difficulty) VALUES (%s, %s, %s, %s);',[s['username'],s['crn'],s['professor_ratings'],s['difficulty']])
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def UpdateUserRatingsAPI(request):
    queryset = ProfessorRatingsFromUser.objects.all()
    user = request.GET.get('username')
    crn = request.GET.get('crn')
    rating = request.GET.get('rating')

    try: 
        # res = queryset.filter(username=user, crn=crn).update(professor_ratings=rating)
        res = ProfessorRatingsFromUser.objects.raw('SELECT * From coursebuddy.Professor_ratings_from_user WHERE Username=%s and CRN = %s;',[user,crn])
        with connection.cursor() as cursor:
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
            # res = queryset.get(username=user, crn=crn).delete()
            res = ProfessorRatingsFromUser.objects.raw('''SELECT * FROM coursebuddy.Professor_ratings_from_user WHERE Username=%s and CRN = %s;''',[user,crn])
            with connection.cursor() as cursor:
                cursor.execute('DELETE FROM coursebuddy.Professor_ratings_from_user WHERE Username=%s and CRN=%s;',[user,crn])
        except res.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        return Response(status=status.HTTP_201_CREATED)

@api_view(['GET'])
def ProfessorWebsiteRatingsAPI(request):
    professor = request.GET.get('professor')
    if request.method == 'GET':
        with connection.cursor() as cursor:
            webdata = scrape(professor)
            if float(webdata['professor_ratings']) > 0:
                serializer = RMPSerializer(data=webdata, context={'request': request})
                if serializer.is_valid():
                    s = serializer.data
                    cursor.execute('INSERT INTO coursebuddy.Professor_ratings_from_websites (professor, professor_ratings) VALUES (%s,%s) ON DUPLICATE KEY UPDATE professor_ratings = %s ;',[s['professor'],s['professor_ratings'], s['professor_ratings']])
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                cursor.execute('SELECT professor, professor_ratings FROM coursebuddy.Professor_ratings_from_websites WHERE professor = %s;',[professor])
                results = namedTuple(cursor)
                if results == []:
                    return Response("Professor rating not avaliable", status=status.HTTP_400_BAD_REQUEST)
                else:
                    ratingSerialize = RMPSerializer(results, context={'request': request}, many=True)
                    return Response(ratingSerialize.data, status=status.HTTP_200_OK)
    return Response(ratingSerialize.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def Spring19GradesAPI(request):
    subject = request.GET.get('subject')
    course = request.GET.get('course')

    # queryset = Sp19.objects.raw('SELECT CRN,a.Professor,AverageGpa,avg_ratings,avg_difficulty FROM coursebuddy.sp19 as a JOIN (SELECT Professor,avg(Professor_ratings) as avg_ratings,avg(Difficulty) as avg_difficulty from coursebuddy.Professor_ratings_from_user as a join coursebuddy.sp19 as b on a.CRN = b.CRN WHERE Course = 411 and Subject = "CS" group by Professor) as b on a.Professor = b.Professor;')
    queryset = Sp19.objects.all()

    try:
        # sections = queryset.filter(subject=subject, course=course)
        sections = Sp19.objects.raw('SELECT * FROM coursebuddy.sp19 WHERE Subject = %s and Course  = %s;',[subject,course])
    except sections.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = Spring19GradesSerializer(sections, context={'request': request}, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def StudyGroupAPI(request):
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
    firstpreference = request.GET.get('first_pref')
    secondpreference = request.GET.get('second_pref')
    thirdpreference = request.GET.get('third_pref')
    try:
        name = Studygroup.objects.raw('CALL test(%s,%s,%s,%s,%s);',[firstpreference,secondpreference,thirdpreference,username,crn])
    except name.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = StudyGroupSerializer(name, context={'request': request}, many=True)
    return Response(serializer.data)

def namedTuple(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

@api_view(['POST','GET'])
def UserRegistrationsAPI(request):

    username = request.GET.get('username')

    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute('SELECT username, major, email, year, crn, subject, course FROM (coursebuddy.StudyGroup natural join coursebuddy.registrations S) NATURAL JOIN coursebuddy.sp19 WHERE Username = %s;',[username])
            results = namedTuple(cursor)
            regserializer = RegistrationSerializer(results, context={'request': request}, many = True)
            return Response(regserializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'POST':
        regserializer = RegistrationSerializer(data=request.data, context={'request': request})
        if regserializer.is_valid():
            s = regserializer.data
            with connection.cursor() as cursor:
                cursor.execute('CALL insertUserData(%s,%s,%s,%s,%s);',[s['username'],s['major'],s['email'],s['year'],s['crn']])
            return Response(regserializer.data, status=status.HTTP_200_OK)
        return Response(regserializer.errors, status=status.HTTP_400_BAD_REQUEST)




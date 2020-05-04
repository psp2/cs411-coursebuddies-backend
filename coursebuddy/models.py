# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Test(models.Model):
    #crn = models.IntegerField()  # Field name made lowercase.
    #professor = models.CharField(primary_key=True, max_length=45)  # Field name made lowercase.
    #averagegpa = models.FloatField()  # Field name made lowercase.
    #professor_ratings = models.FloatField()  # Field name made lowercase.
    #difficulty = models.FloatField() 

    crn = models.IntegerField(db_column='CRN')  # Field name made lowercase.
    professor = models.CharField(db_column='Professor', primary_key=True, max_length=45) 
    averagegpa = models.FloatField(db_column='AverageGpa', blank=True, null=True)  # Field name made lowercase.
    professor_ratings = models.FloatField(db_column='Professor_ratings', blank=True, null=True)  # Field name made lowercase.
    difficulty = models.CharField(db_column='Difficulty', max_length=45, blank=True, null=True)  # Field name made lowercase.



class ProfessorRatingsFromUser(models.Model):
    username = models.CharField(db_column='Username', max_length=45)  # Field name made lowercase.
    crn = models.IntegerField(db_column='CRN')  # Field name made lowercase.
    professor_ratings = models.FloatField(db_column='Professor_ratings', blank=True, null=True)  # Field name made lowercase.
    difficulty = models.CharField(db_column='Difficulty', max_length=45, blank=True, null=True)  # Field name made lowercase.
    id = models.AutoField(db_column='id', primary_key=True)

    class Meta:
        managed = False
        db_table = 'Professor_ratings_from_user'
        #unique_together = (('username', 'crn'),)


class ProfessorRatingsFromWebsites(models.Model):
    professor = models.CharField(db_column='Professor', primary_key=True, max_length=45)  # Field name made lowercase.
    professor_ratings = models.FloatField(db_column='Professor_ratings', blank=True, null=True)  # Field name made lowercase.
    total = models.IntegerField(db_column='Total', blank=True, null=True)  # Field name made lowercase.
    difficulty = models.FloatField(db_column='Difficulty', blank=True, null=True)  # Field name made lowercase.
    crn = models.IntegerField(db_column='CRN')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Professor_ratings_from_websites'
        unique_together = (('professor', 'crn'),)

class Studygroup(models.Model):
    username = models.CharField(db_column='Username', primary_key=True,max_length=45)  # Field name made lowercase.
    major = models.CharField(db_column='Major', max_length=45)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=45)  # Field name made lowercase.
    year = models.CharField(db_column='Year', max_length=45)  # Field name made lowercase.
    crn = models.IntegerField(db_column='CRN')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'StudyGroup'
        unique_together = (('username', 'crn'),)


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Login(models.Model):
    username = models.CharField(primary_key=True, max_length=45)
    password = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'login'


class Sp19(models.Model):
    subject = models.CharField(db_column='Subject', max_length=10, blank=True, null=True)  # Field name made lowercase.
    course = models.IntegerField(db_column='Course', blank=True, null=True)  # Field name made lowercase.
    crn = models.IntegerField(db_column='CRN', primary_key=True)  # Field name made lowercase.
    coursetitle = models.CharField(db_column='CourseTitle', max_length=45, blank=True, null=True)  # Field name made lowercase.
    schedtype = models.CharField(db_column='SchedType', max_length=45, blank=True, null=True)  # Field name made lowercase.
    a_field = models.IntegerField(db_column='A+', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    a = models.IntegerField(db_column='A', blank=True, null=True)  # Field name made lowercase.
    a_field_0 = models.IntegerField(db_column='A-', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'. Field renamed because of name conflict.
    b_field = models.IntegerField(db_column='B+', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    b = models.IntegerField(db_column='B', blank=True, null=True)  # Field name made lowercase.
    b_field_0 = models.IntegerField(db_column='B-', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'. Field renamed because of name conflict.
    c_field = models.IntegerField(db_column='C+', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    c = models.IntegerField(db_column='C', blank=True, null=True)  # Field name made lowercase.
    c_field_0 = models.IntegerField(db_column='C-', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'. Field renamed because of name conflict.
    d_field = models.IntegerField(db_column='D+', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    d = models.IntegerField(db_column='D', blank=True, null=True)  # Field name made lowercase.
    d_field_0 = models.IntegerField(db_column='D-', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'. Field renamed because of name conflict.
    f = models.IntegerField(db_column='F', blank=True, null=True)  # Field name made lowercase.
    w = models.IntegerField(db_column='W', blank=True, null=True)  # Field name made lowercase.
    averagegpa = models.FloatField(db_column='AverageGpa', blank=True, null=True)  # Field name made lowercase.
    professor = models.CharField(db_column='Professor', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sp19'

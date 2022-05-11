from django.db import models, connection
from passlib.hash import pbkdf2_sha256
# from django.contrib import auth

# Create your models here.
class Users(models.Model):
    user_id = models.CharField(primary_key=True, max_length=255)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=12)
    city = models.CharField(max_length=255)
    birth_date = models.DateField()
    # profile_pic = models.ImageField(upload_to='images/', blank=True)
    
    class Meta:
        managed = False
        db_table = 'users'

    def __str__(self):
        return "@{}".format(self.user_id)

    def get_user_by_user_id(user_id):
        return Users.objects.raw("SELECT * FROM users WHERE user_id = %s;", [user_id])

    def get_user_by_email(email):
        return Users.objects.raw("SELECT * FROM users WHERE email = %s;", [email])

    def is_user_duplicate(**dict):
        message = ''
        if 'user_id' in dict.keys():
            user_id = dict['user_id']
            temp_result = Users.get_user_by_user_id(user_id)
            if temp_result:
                message = 'The UserID: {} is occupied, please use another UserID'.format(user_id)
                return message, True
        if 'email' in dict.keys():
            email = dict['email']
            temp_result = Users.get_user_by_email(email)
            if temp_result:
                message = 'The Email: {} is occupied, please use another Email'.format(email)
                return message, True
        return message, False

    def verify_password(self, raw_password):
        return pbkdf2_sha256.verify(raw_password, self.password)

    def create_new_user(user_id: str, password: str, first_name: str,
                        last_name: str, gender: str, email: str, phone: str, city: str, birth_date: str):
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO users (user_id, password, first_name, last_name, gender, email, phone, city, birth_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", 
            [user_id, password, first_name, last_name, gender, email, phone, city, birth_date])

    def update_user_by_user_id(old_user_id: str, user_id: str, password: str, first_name: str,
                        last_name: str, gender: str, email: str, phone: str, city: str, birth_date: str):
        
        Users.objects.filter(user_id=old_user_id).update(user_id=user_id, password=password, first_name=first_name,
                last_name=last_name, gender=gender, email=email, phone=phone, city=city, birth_date=birth_date)
        with connection.cursor() as cursor:
            cursor.execute("UPDATE users SET user_id=%s, password=%s, first_name=%s, last_name=%s, gender=%s, email=%s, phone=%s, city=%s, birth_date=%s WHERE user_id = %s;", 
                [user_id, password, first_name, last_name, gender, email, phone, city, birth_date, old_user_id])

class Preference(models.Model):
    users_id = models.OneToOneField('Users', models.DO_NOTHING, primary_key=True)
    outdoor_love_type = models.CharField(max_length=255)
    food_preference = models.CharField(max_length=255)
    budget_type = models.CharField(max_length=255)
    art_type = models.CharField(max_length=255)
    museum_type = models.CharField(max_length=255)
    city_trip_type = models.CharField(max_length=255)
    transportation_type = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'preference'

class Personalpic(models.Model):
    personal_img = models.ImageField(upload_to='images/')

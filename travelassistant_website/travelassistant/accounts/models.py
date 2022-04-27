from django.db import models, connection
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
        return Users.objects.raw("SELECT * FROM users WHERE user_id = '{}';".format(user_id))

    def get_user_by_email(email):
        return Users.objects.raw("SELECT * FROM users WHERE email = '{}';".format(email))

    def is_user_duplicate(**dict):
        message = ''
        for item in dict.items():
            temp_result = Users.objects.raw("SELECT * FROM users WHERE {}='{}';".format(item[0], item[1]))
            if temp_result:
                message = 'The {a}: {r} is occupied, please choose another {a}'.format(a=item[0].upper(), r=item[1])
                return message, True
        return message, False

    # def is_user_duplicate(user_id, email):
    #     message = ''
    #     temp_result = Users.get_user_by_user_id(user_id)
    #     if temp_result:
    #         message = 'The UserID: {} is occupied, please use another UserID'.format(user_id)
    #         return message, True
    #     temp_result = Users.get_user_by_email(email)
    #     if temp_result:
    #         message = 'The Email: {} is occupied, please use another Email'.format(email)
    #         return message, True
    #     return message, False

    def create_new_user(user_id: str, password: str, first_name: str,
                        last_name: str, gender: str, email: str, phone: str, city: str, birth_date: str):
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO users (user_id, password, first_name, last_name, gender, email, phone, city, birth_date) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
                user_id, password, first_name,
                last_name, gender, email, phone, city, birth_date))

    def update_user_by_user_id(old_user_id: str, user_id: str, password: str, first_name: str,
                        last_name: str, gender: str, email: str, phone: str, city: str, birth_date: str):
        with connection.cursor() as cursor:
            cursor.execute("UPDATE users SET user_id='{}', password='{}', first_name='{}', last_name='{}', gender='{}', email='{}', phone='{}', city='{}', birth_date='{}' WHERE user_id = '{}';".format(
                user_id, password, first_name,
                last_name, gender, email, phone, city, birth_date, old_user_id))

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

from django.db import models
import re
import bcrypt


class UserManager(models.Manager):
    def r_validator(self, post_data):
        errors = {}
        if len(post_data['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters"
        if len(post_data['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters"

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Not a valid email"

        if len(post_data['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"

        if post_data['password'] != post_data['confirm_password']:
            errors['confirm_password'] = "password does not match confirm password"

        if len(User.objects.filter(email=post_data['email'])) > 0:
            errors['email'] = "Email already exists"

        return errors

    def l_validator(self, post_data):
        errors = {}
        potential_users = User.objects.filter(email=post_data['login_email'])
        if len(potential_users) == 0:
            errors['login_email'] = "Email does not exist. Please sign up!"
        else:
            user = potential_users[0]
            if not bcrypt.checkpw(post_data['login_password'].encode(), user.password.encode()):
                errors['login_password'] = "Invalid Password"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    date_hired = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


# class EventManager(models.Manager):
#     def create_validator(self, post_data):
#         errors = {}
#         if len(post_data['title']) < 3:
#             errors['title'] = "Title must be at least 3 characters long"
#         if len(post_data['description']) == 0:
#             errors['description'] = "Description cannot be blank"
#       return errors


class Item(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    creator = models.ForeignKey(User, related_name="created_events", on_delete=models.CASCADE)
    guests = models.ManyToManyField(User, related_name="attending_events")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #objects = EventManager()

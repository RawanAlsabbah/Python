from django.db import models
import re
import bcrypt
from datetime import datetime, timedelta
# Create your models here.


class UserManager(models.Manager):
    def register_validator(self, post_data):
        errors = {}
        # check first name 2 char
        if len(post_data['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters, yo"
        # check last name 2 char
        if len(post_data['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters, yo"
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Invalid email format"
        # check password char len 8
        if len(post_data['password']) < 8:
            errors['password'] = "Password must be at least 8 characters, please"
        # check confirm password == password
        if post_data['password'] != post_data['confirm_pw']:
            errors['confirm_pw'] = "Confirm password does not match Password"
        print("reached the validator for register")
        return errors

    def login_validator(self, post_data):
        errors = {}
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Invalid email format"
        # check password char len 8
        if len(post_data['password']) < 8:
            errors['password'] = "Password must be at least 8 characters, please"
        # check if email is in db
        user_list = User.objects.filter(email=post_data['email'])
        if len(user_list) == 0:
            errors['email2'] = "Email was not found in db"
        elif not bcrypt.checkpw(post_data['password'].encode(), user_list[0].password.encode()):
            errors['match'] = "Password does not match the db"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45, unique=True)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class JobManager(models.Manager):
    def job_validator(self, post_data , ):
        errors = {}
        if len(post_data["title"]) < 1:
                errors["title"] = "Title  is required "
        elif len(post_data['title']) < 3:
            errors['title'] = "Title must be at least 3 characters"
        if len(post_data["desc"]) < 1:
                errors["desc"] = "Description is required "
        elif len(post_data['desc']) < 3:
            errors['desc'] = "Description must be at least 3 characters"
        if len(post_data["location"]) < 1:
                    errors["location"] = "location is required "
        elif len(post_data['location']) < 3:
            errors['location'] = "location must be at least 3 characters"
        if len(post_data.getlist('category')) < 1:
                    errors["category"] = "category  is required "
        
        return errors


class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    location=models.CharField(max_length=255)
    posted_by = models.ForeignKey(User, related_name="jobs", on_delete=models.CASCADE)
    add_job= models.ManyToManyField(User, related_name="add_jobs")
    give_up=models.BooleanField(default=True)
    category=models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = JobManager()


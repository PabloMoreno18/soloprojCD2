from django.db import models
import re
#import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.
class app_manager(models.Manager):
    def user_validator(self, postData):
        errors = []

        if len(postData['fname']) < 2:
            errors.append("First name should be at least 2 characters")
        if len(postData['lname']) < 2:
            errors.append("Last name should be at least 2 characters")
        if len(postData['password']) < 8:
            errors.append("Password must be at least 8 characters")
        if postData['password'] != postData['pw_confirm']:
            errors.append("Passwords do not match!")
        if not EMAIL_REGEX.match(postData['email']):
            errors.append("Invalid email address!")
        return errors

    def post_validate(self, postData):
        errors = []
        
        if len(postData['gtitle']) < 3:
            errors.append("Game title should not be less than 3 characters")
        if len(postData['desc']) < 5:
            errors.append("Game description should be at least 5 characters")
        return errors

class User(models.Model):
    #id
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = app_manager()

class Game(models.Model):
    #id
    title = models.CharField(max_length=100)
    description = models.TextField()
    rating = models.CharField(max_length=25)
    platform = models.CharField(max_length=55)
    created_by = models.ForeignKey(User, related_name = "created_game", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = app_manager()

class Comment(models.Model):
    comment = models.CharField(max_length=255)
    creator = models.ForeignKey(User, related_name='user_comments', on_delete=models.CASCADE)
    wall_message = models.ForeignKey(Game, related_name="post_comments", on_delete=models.CASCADE)
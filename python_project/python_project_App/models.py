from django.db import models

# Create your models here.
from errno import EROFS
from urllib import request
import re
import bcrypt


class UserManger (models.Manager):
    def validator(self, PostData):
        errors = {}
        if len(PostData['first_name']) < 2:
            errors['first_name'] = 'first name should be at least 2 characters'
        if len(PostData['last_name']) < 2:
            errors['last_name'] = 'last name should be at least 2 characters'
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(PostData['email']):
            errors['email'] = "Invalid email address!"
        if len(PostData['password']) < 8:
            errors['password'] = 'password should be at least 8 characters'
        if not PostData['password'] == PostData['confirm_pw']:
            errors['confirm_pw'] = 'Password and confirm should be match'

        return errors


class Users(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManger()


class Note(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    user = models.ForeignKey(
        Users, related_name='my_note', on_delete=models.CASCADE)


class Posts(models.Model):
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    user = models.ForeignKey(
        Users, related_name='user_post', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comments(models.Model):
    comment = models.TextField()
    post = models.ForeignKey(
        Posts, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(
        Users, related_name="user_comment", on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(Users, related_name="liked")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Algorithm(models.Model):
    created_by = models.ForeignKey(
    Users, related_name="user_algorithms", on_delete=models.CASCADE)
    desc = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Todo(models.Model):
    todo = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(
        Users, related_name='user_todo', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Image(models.Model):
    photo = models.ImageField(upload_to='All_files/images/')
    image = models.ImageField(
        upload_to=None, height_field=None, width_field=None, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class File(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='All_files/files/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)

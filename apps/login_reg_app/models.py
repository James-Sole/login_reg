# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^[a-zA-Z0-9]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self,postData):
        errors = {}
        if len(postData['first_name'])<2:
            errors['first_name']= 'User first name should be more than 2 characters'
        if not NAME_REGEX.match(postData['first_name']):
            errors['first_name_re']= 'User first name should not contain numbers or simbols'
        if len(postData['last_name'])<2:
            errors['last_name']= 'User last name should be more than 2 characters'
        if not NAME_REGEX.match(postData['last_name']):
            errors['last_name_re']= 'User last name should not contain numbers or simbols'
        if len(postData['password'])<8:
            errors['password']= 'password should be more than 8 characters'
        if not PASSWORD_REGEX.match(postData['password']):
            errors['password_re']= 'password should contain on numbers and characters'
        if postData['password'] != postData['conf_password']:
            errors['conf_password']= 'password should match confirmation password'
        if not EMAIL_REGEX.match(postData['email']):
            errors['email_re']= 'Invalid email'

        return errors
    def login_validator(self,postData):
        errors = {}
        user = User.objects.get(email = postData['email'])
        if postData['email'] == User.email:
            password = user.password
            if not bcrypt.checkpw(postData['password'].encode(), password.encode()):
                error['password'] = 'Incorrect Email/Password'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    objects = UserManager()

# Create your models here.

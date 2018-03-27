# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import re

import bcrypt

from time import time, strftime, localtime, strptime

REGEX_EMAIL = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


# Create your models here.

class UserManager(models.Manager):
    def RegisterValidator(self, postData):

        response = {}
        response['isValid'] =True
        response['errors'] = []
        response['user'] = None

        # name check
        if len(postData['name']) <1:
            response['errors'].append("Please fill in name field")
        elif len(postData['name']) <2:
            response['errors'].append("Name field must be at least two characters")
        elif str.isalpha(str(postData['name'])) ==False:
            response['errors'].append("Name field may only contain alphabetic characters")

        #alias check
        if len(postData['alias']) <1:
            response['errors'].append("Please provide an alias to use on our site")

        #email check
        if len(postData['email']) <1:
            response['errors'].append("Please fill in email field")
        elif REGEX_EMAIL.match(postData['email']) == None:
            response['errors'].append("Email format invalid")
        elif len(User.objects.filter(email = postData['email'])) > 0:
            response['errors'].append("Email already exists. Please login")

        # birthday check

        if len(postData['birthday']) <1:
          response['errors'].append("Please enter a birthday")

        if len(postData['birthday']) >0:
          now = strftime("%Y-%m-%d", localtime())
          now_2 = strptime(now, "%Y-%m-%d")
          bday = strptime(postData['birthday'], "%Y-%m-%d")
          if bday>now_2:
              response['errors'].append("Birthday may not be in the future")

        #password check:
        if len(postData['password']) <1:
            response['errors'].append("Password required")
        elif len(postData['password']) <8:
            response['errors'].append("Password must be at least 8 characters")
        elif postData['password'] != postData['confirm_password']:
            response['errors'].append("Passwords do not match")

        if len(response['errors']) >0:
            response['isValid'] = False

        else:
            #password encrypt if no errors
            hash1 = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            print hash1
            #create new user, to be passed through the response dictionary
            response['user'] = User.objects.create(
                name = postData['name'],
                alias = postData['alias'],
                email = postData['email'],
                birthday = postData['birthday'],
                password = hash1
                )

        #returning response dictionary
        return response

    def LoginValidator(self, postData):

        response = {}
        response['isValid'] =True
        response['errors'] = []
        response['user'] = None

        #email check:
        if len(postData['email']) <1:
            response['errors'].append("Please fill in email field")
        elif REGEX_EMAIL.match(postData['email']) == None:
            response['errors'].append("Email format invalid")
            
        #check to see if email is in system
        elif len(User.objects.filter(email = postData['email'])) <1:
            response['errors'].append("Email does not exist. Please register.")

        #password check
        if len(postData['password']) <1:
            response['errors'].append("Password required")

        #password hash comparison
        if len(response['errors']) <1:
            user = User.objects.filter(email=postData['email'])
            if bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
                print "PWs match"
                response['user'] = user[0]

            else:
                response['errors'].append("Password incorrect")

        if len(response['errors']) >0:
            response['isValid'] = False

        return response

class QuoteManager(models.Manager):

	def QuoteValidator(self, postData):

		response = {}
		response['isValid'] = True
		response['errors'] = []
		

		#quote field check
		if len(postData['quote']) < 10:
			response['errors'].append("Quote must be at least 10 characters long")

		if len(postData['source']) <3:
			response['errors'].append("Quote source must be at least 3 characters long")

		print len(response['errors'])

		#check to see if validation parameters are met
		if len(response['errors']) >0:
			response['isValid'] = False

		return response

#classes
class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birthday = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #if validating, remember to pass it through the approprate manager
    objects =UserManager()

    def __repr__(self):
        return "name: {}, alias: {}, email: {}".format(self.name, self.alias, self.email)

class Quote(models.Model):
    quote = models.TextField()
    source = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uploader = models.ForeignKey(User, related_name="uploaded_quotes")

    #if validating, remember to pass it through the approprate manager
    objects =QuoteManager()

    def __repr__(self):
        return "quote: {}, source: {}, uploader: {}".format(self.quote, self.source, self.uploader)

class Favorite(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    favoritor = models.ForeignKey(User, related_name="favorites")
    favorited = models.ForeignKey(Quote, related_name="favorites")

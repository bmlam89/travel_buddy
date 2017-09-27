# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
# Create your models here.
class Validator(models.Manager):
    def is_valid(self,post):
        errors = {}
        if len(post["name"]) < 3 or not post["name"].isalpha():
            errors["name"] = "Name must be at least 3 characters and contain only alphabetical letters."
        if len(post["username"]) < 3 or not post["username"].isalpha():
            errors["username"] = "Username must be at least 3 characters and contain only alphabetical letters."
        if len(post["password"]) < 8:
            errors["password"] = "Password must be at least 8 characters."
        if post["password"] != post["confirm"]:
            errors["confirm"] = "Passwords don't match."

        return errors
    def valid_trip(self,post):
        errors = {}
        if type(post.get("destination")) is None:
            errors["destination"] = "Destination field must not be empty"
        if type(post.get("description")) is None:
            errors["description"] = "Description field must not be empty"
        if type(post.get("from")) is None or type(post.get("to")) is None or post["from"] > post["to"]:
            errors["date"] = "Invalid date input"

        return errors


class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = Validator()

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    departure_date = models.DateField()
    return_date = models.DateField()
    desc = models.CharField(max_length=255)
    user = models.ForeignKey(User,related_name="trips")
    shared_users = models.ManyToManyField(User,related_name="shared_trips")
    objects = Validator()
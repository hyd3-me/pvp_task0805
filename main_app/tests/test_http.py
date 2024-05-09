from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
import datetime
from unittest import skip
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

#from noteqq import test_data
from main_app.tests.test_base_http import BaseUser
from main_app import utils, data_app
from main_app import forms
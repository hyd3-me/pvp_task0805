from django.test import TestCase, TransactionTestCase
from django.http import HttpRequest
from django.utils import timezone
from unittest import skip
from datetime import timedelta

#from noteqq import test_data
from main_app import utils
from main_app import data_app


class UserTest(TestCase):

    def test_create_user(self):
        s, user1 = utils.create_user(data_app.USER1)
        self.assertEqual(user1.username, data_app.USER1[0])

    def test_create_user_with_ref_code(self):
        s, user1 = utils.create_user(data_app.USER1)
        ref_code = user1.profile.ref_code
        s, user2 = utils.create_user((*data_app.USER2, ref_code))
        self.assertEqual(user2.username, data_app.USER2[0])
        self.assertEqual(user2.refl.first().referrer.username, user1.username)
        self.assertEqual(user2.refl.first().referrer.profile.ref_code, ref_code)
    
    def test_get_user_by_id(self):
        s, user1 = utils.create_user(data_app.USER1)
        user_from_bd = utils.get_user_by_id(user1.id)
        self.assertEqual(user1, user_from_bd)
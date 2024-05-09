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
    
    def test_get_referals_from_user(self):
        s, user1 = utils.create_user(data_app.USER1)
        ref_code = user1.profile.ref_code
        s, user2 = utils.create_user((*data_app.USER2, ref_code))
        s, user3 = utils.create_user((*data_app.USER3, ref_code))
        status, refs = utils.get_referals_by_user(user1)
        self.assertTrue(status)
        self.assertEqual(len(refs), 2)
    
    def test_get_all_referals(self):
        s, user1 = utils.create_user(data_app.USER1)
        ref_code = user1.profile.ref_code
        s, user2 = utils.create_user((*data_app.USER2, ref_code))
        s, user3 = utils.create_user((*data_app.USER3, ref_code))
        s, user4 = utils.create_user(data_app.USER4)
        ref_code = user4.profile.ref_code
        s, user5 = utils.create_user((*data_app.USER5, ref_code))
        s, user6 = utils.create_user((*data_app.USER6, ref_code))
        status, refs = utils.get_all_referals()
        self.assertTrue(status)
        self.assertEqual(len(refs), 4)
    
    def test_get_money(self):
        s, user1 = utils.create_user(data_app.USER1)
        self.assertEqual(user1.profile.balance, 0)
        s, resp1 = utils.get_money(user1)
        self.assertEqual(user1.profile.balance, 9999)
    
    def test_can_buy_thin(self):
        s, user1 = utils.create_user(data_app.USER1)
        s, resp1 = utils.get_money(user1)
        req = 100
        s, resp1 = utils.buy_thing(user1, req)
        s, balance1 = utils.get_balance_by_user(user1)
        self.assertEqual(9999 - 100, balance1)
    
    def test_can_get_referral(self):
        s, user1 = utils.create_user(data_app.USER1)
        ref_code = user1.profile.ref_code
        s, user2 = utils.create_user((*data_app.USER2, ref_code))
        s, ref = utils.is_refl(user2)
        s, user3 = utils.create_user((*data_app.USER3, ''))
        s, ref = utils.is_refl(user3)
        if s: print(ref.referrer)
    
    def test_can_control_buy_from_refl(self):
        s, user1 = utils.create_user(data_app.USER1)
        ref_code = user1.profile.ref_code
        s, user2 = utils.create_user((*data_app.USER2, ref_code))
        s, resp1 = utils.get_money(user2)
        req = 100
        s, resp1 = utils.buy_thing(user2, req)
        req = 200
        s, resp1 = utils.buy_thing(user2, req)
        s, ref = utils.is_refl(user2)
        self.assertEqual(ref.total_amount, 100 + 200)
        self.assertEqual(ref.num_purchases, 2)
from django.test import TestCase
from django.urls import reverse
from unittest import skip
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from main_app import utils, data_app


def create_ref_link(ref_code):
    domain = 'localhost'
    return f'http://{domain}:8000{reverse(data_app.REG_PATH)}?ref={ref_code}'

class BaseUser(TestCase):

    def reg_me(self, user_tuple=data_app.USER1):
        resp1 = self.client.post(reverse(data_app.REG_PATH), {
            'username': user_tuple[0],
            'password':user_tuple[1],
            'password':user_tuple[1]}, follow=True)
        return resp1

    def login(self, user_tuple=data_app.USER1):
        resp1 = self.client.post(reverse(data_app.LOGIN_PATH), {
            'username': user_tuple[0],
            'password': user_tuple[1]}, follow=True)
        return resp1

    def logout(self):
        resp1 = self.client.get(reverse(data_app.LOGOUT_PATH), follow=True)
        return resp1

    def make_user_and_login(self, user_tuple=data_app.USER1, p_login=True):
        s, user1 = utils.create_user(user_tuple)
        if p_login: resp1 = self.login(user_tuple)
        return True, user1

class UserTest(BaseUser):

    def test_redirect_after_register_user(self):
        resp1 = self.reg_me()
        self.assertRedirects(resp1, reverse(data_app.PROFILE_PATH))
    
    def test_can_get_ref_code(self):
        s, user1 = utils.create_user(data_app.USER1)
        ref_code = utils.get_ref_code(user1)
        ref_link = create_ref_link(ref_code)
        resp1 = self.client.get(ref_link)
        self.assertContains(resp1, ref_code)
    
    def test_can_reg_from_ref_code(self):
        s, user1 = utils.create_user(data_app.USER1)
        ref_code = utils.get_ref_code(user1)
        ref_link = create_ref_link(ref_code)
        user_tuple = data_app.USER2
        resp1 = self.client.post(ref_link, {
            'username': user_tuple[0],
            'password': user_tuple[1],
            'ref_code': ref_code}, follow=True)
        self.assertRedirects(resp1, reverse(data_app.PROFILE_PATH))
        return resp1
    
    def test_ref_code_in_profile_page(self):
        resp1 = self.test_can_reg_from_ref_code()
        user2 = utils.get_user_by_id(2)
        ref_code = utils.get_ref_code(user2)
        ref_link = create_ref_link(ref_code)
        self.assertContains(
            resp1, f'<p>my ref_link: {ref_link}</p>', html=True)

    def test_myrefs_link_in_profile_page(self):
        resp1 = self.test_can_reg_from_ref_code()
        self.assertContains(
            resp1, f'<p><a href={reverse(data_app.REFERRAL_PATH)}>my referals</a></p>', html=True)

    def test_can_view_own_referals(self):
        s, user1 = utils.create_user(data_app.USER1)
        ref_code = user1.profile.ref_code
        s, user2 = utils.create_user((*data_app.USER2, ref_code))
        s, user3 = utils.create_user((*data_app.USER3, ref_code))
        self.login(data_app.USER1)
        resp1 = self.client.get(reverse(data_app.REFERRAL_PATH))
        self.assertContains(resp1, f'{data_app.USER2[0]}')
        self.assertContains(resp1, f'{data_app.USER3[0]}')
    
    def test_allrefs_link_in_profile_page(self):
        resp1 = self.test_can_reg_from_ref_code()
        self.assertContains(
            resp1, f'<p><a href={reverse(data_app.ALL_REFS_PATH)}>all refs</a></p>', html=True)
    
    def test_can_view_all_referals(self):
        # + referrer
        s, user1 = utils.create_user(data_app.USER1)
        # user1 ref_code
        ref_code = user1.profile.ref_code
        # +2 referrals
        s, user2 = utils.create_user((*data_app.USER2, ref_code))
        s, user3 = utils.create_user((*data_app.USER3, ref_code))

        s, user4 = utils.create_user(data_app.USER4)
        ref_code = user4.profile.ref_code
        s, user5 = utils.create_user((*data_app.USER5, ref_code))
        s, user6 = utils.create_user((*data_app.USER6, ref_code))

        self.login(data_app.USER1)
        resp1 = self.client.get(reverse(data_app.ALL_REFS_PATH))
        # check to all refs in page
        self.assertContains(resp1, f'{data_app.USER2[0]}')
        self.assertContains(resp1, f'{data_app.USER3[0]}')
        self.assertContains(resp1, f'{data_app.USER5[0]}')
        self.assertContains(resp1, f'{data_app.USER6[0]}')
    
    def test_buypage_link_in_profile_page(self):
        resp1 = self.test_can_reg_from_ref_code()
        self.assertContains(
            resp1, f'<p><a href={reverse(data_app.BUY_PATH)}>buy page</a></p>', html=True)
    
    def test_can_view_buy_page(self):
        s, user1 = utils.create_user(data_app.USER1)
        self.login(data_app.USER1)
        resp1 = self.client.get(reverse(data_app.BUY_PATH))
        self.assertTemplateUsed(resp1, 'buy_page.html')
    
    def test_buy_page_have_balance(self):
        s, user1 = utils.create_user(data_app.USER1)
        s, balance1 = utils.get_balance_by_user(user1)
        self.login(data_app.USER1)
        resp1 = self.client.get(reverse(data_app.BUY_PATH))
        self.assertContains(
            resp1, f'<p>my balance: {balance1:.2f}</p>', html=True)
        s, resp1 = utils.get_money(user1)
        resp1 = self.client.get(reverse(data_app.BUY_PATH))
        s, balance1 = utils.get_balance_by_user(user1)
        self.assertContains(
            resp1, f'<p>my balance: {balance1:.2f}</p>', html=True)
    
    def test_give_money(self):
        s, user1 = utils.create_user(data_app.USER1)
        s, balance1 = utils.get_balance_by_user(user1)
        self.login(data_app.USER1)
        resp1 = self.client.get(reverse(data_app.GIVE_MONEY_PATH), follow=True)
        self.assertRedirects(resp1, reverse('buy_page'))
        s, balance1 = utils.get_balance_by_user(user1)
        self.assertContains(
            resp1, f'<p>my balance: {balance1:.2f}</p>', html=True)
    
    def test_can_buy_thing(self):
        s, user1 = utils.create_user(data_app.USER1)
        s, resp1 = utils.get_money(user1)
        self.login(data_app.USER1)
        resp1 = self.client.post(reverse('post_buy'), {
            'amount': 100}, follow=True)
        self.assertRedirects(resp1, reverse(data_app.HOME_PATH))
        s, balance1 = utils.get_balance_by_user(user1)
        self.assertEqual(balance1, 9999-100)
    
    def test_pay_to_referrer(self):
        s, user1 = utils.create_user(data_app.USER1)
        ref_code = utils.get_ref_code(user1)
        ref_link = create_ref_link(ref_code)
        user_tuple = data_app.USER2
        resp1 = self.client.post(ref_link, {
            'username': user_tuple[0],
            'password': user_tuple[1],
            'ref_code': ref_code}, follow=True)
        self.login(data_app.USER2)
        user2 = utils.get_user_by_id(2)
        s, resp1 = utils.get_money(user2)
        AMOUNT = 100
        resp1 = self.client.post(reverse('post_buy'), {
            'amount': AMOUNT}, follow=True)
        percent5 = 0.05 * AMOUNT
        s, balance1 = utils.get_balance_by_user(user1)
        self.assertEqual(balance1, percent5)
    
    def test_can_view_refs_purchases(self):
        s, user1 = utils.create_user(data_app.USER1)
        ref_code = user1.profile.ref_code
        s, user2 = utils.create_user((*data_app.USER2, ref_code))
        s, resp1 = utils.get_money(user2)
        req = 100
        s, resp1 = utils.buy_thing(user2, req)
        req = 200
        s, resp1 = utils.buy_thing(user2, req)
        s, user3 = utils.create_user((*data_app.USER3, ref_code))
        s, resp1 = utils.get_money(user3)
        req = 500
        s, resp1 = utils.buy_thing(user3, req)
        req = 200
        s, resp1 = utils.buy_thing(user3, req)
        self.login(data_app.USER1)
        resp1 = self.client.get(reverse(data_app.REFERRAL_PATH))
        self.assertContains(resp1, f'{100 + 200}')
        self.assertContains(resp1, f'{500 + 200}')
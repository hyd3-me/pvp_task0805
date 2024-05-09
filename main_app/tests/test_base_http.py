from django.test import TestCase
from django.urls import reverse
from unittest import skip
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from main_app import utils, data_app


def create_ref_link(ref_code):
    domain = 'localhost'
    return f'https://{domain}{reverse(data_app.REG_PATH)}?={ref_code}'

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
    
    def test_can_reg_from_ref_code(self):
        s, user1 = utils.create_user(data_app.USER1)
        ref_code = utils.get_ref_code(user1)
        ref_link = create_ref_link(ref_code)
        user_tuple = data_app.USER2
        resp1 = self.client.post(ref_link, {
            'username': user_tuple[0],
            'password': user_tuple[1],
            'password': user_tuple[1]}, follow=True)
        self.assertRedirects(resp1, reverse(data_app.PROFILE_PATH))
        return resp1
    
    def test_ref_code_in_profile_page(self):
        resp1 = self.test_can_reg_from_ref_code()
        user2 = utils.get_user_by_id(2)
        ref_code = utils.get_ref_code(user2)
        ref_link = create_ref_link(ref_code)
        self.assertContains(
            resp1, f'<p>my ref_link: {ref_link}</p>', html=True)
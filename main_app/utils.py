from django.contrib.auth.models import User
from uuid import uuid4
from decimal import Decimal

from .models import Profile, Referral


def try_me(fn):
    try:
        return fn
    except Exception as e:
        #logger.error(e)
        return False, e

def create_user(data):
    #username, password, uuid_code = data
    user = User.objects.create_user(username=data[0], password=data[1])
    if user:
        profile, created = Profile.objects.get_or_create(user=user)
        if data[2]:
            refr = Profile.objects.get(ref_code=data[2])
            if not refr:
                return False, 'error: not user 4 this ref_code'
            referral = Referral(referrer=refr.user, referral=user)
            referral.save()
        return True, user
    return False, 'error in func: create_user'

def get_ref_code(user_obj):
    return user_obj.profile.ref_code

def get_user_by_id(user_id):
    return User.objects.get(id=user_id)

def get_referals_by_user(user_obj):
    try:
        return True, user_obj.refr.all()
    except Referral.DoesNotExist as e:
        return False, e

def get_all_referals():
    return True, Referral.objects.all()

def get_money(user_obj):
    user_obj.profile.balance += 9999
    user_obj.profile.save()
    #user_obj.save()
    return True, user_obj

def get_balance_by_user(user_obj):
    user_obj.profile.refresh_from_db()
    return True, user_obj.profile.balance

def is_refl(user_obj):
    try:
        return True, Referral.objects.get(referral=user_obj)
    except Referral.DoesNotExist as e:
        return False, e

def get_referrer(user_obj):
    try:
        return True, Referral.objects.get(referral=user_obj)
    except Referral.DoesNotExist as e:
        return False, e

def process_buy(ref_obj, amount):
    ref_obj.total_amount += amount
    ref_obj.num_purchases += 1
    ref_obj.save()

def give_bonus(ref_obj, pay):
    percent5 = 0.05 * float(pay)
    ref_obj.referrer.profile.balance += Decimal.from_float(percent5)
    ref_obj.referrer.profile.save()
    return True, ref_obj

def buy_thing(user_obj, req):
    #valid balance pass
    if req > user_obj.profile.balance:
        return False, 'not enough'
    user_obj.profile.balance -= req
    user_obj.profile.save()
    #add thing to store pass
    #if referral then give bonus
    s, resp1 = is_refl(user_obj)
    if s:
        process_buy(resp1, req)
        give_bonus(resp1, req)
    return True, user_obj

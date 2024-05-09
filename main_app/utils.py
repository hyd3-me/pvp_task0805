from django.contrib.auth.models import User
from uuid import uuid4

from .models import Profile, Referral

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
    return True, user_obj.refr.all()

def get_all_referals():
    return True, Referral.objects.all()
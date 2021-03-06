
from django.contrib.auth.models import Group, User
from django.shortcuts import redirect
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.views.decorators.cache import never_cache
from psikolog.models import CustomUserModel
from django.contrib.auth import login as auth_login
from social_core.actions import do_auth, do_complete, do_disconnect

USER_FIELDS = ['username', 'email']

def create_user(strategy, details, backend, user=None, *args, **kwargs):
    print("CREATE USER CALLED") 
    print(details)
    print(strategy)
    print(backend)
    isExist=CustomUserModel.objects.filter(email=details["email"])
    if isExist:
        auth_login(backend, isExist.first())
        return redirect("index")
    

    if user:
        return {'is_new': False}

    fields = dict((name, kwargs.get(name, details.get(name)))
                  for name in backend.setting('USER_FIELDS', USER_FIELDS))

    try:
        if User.objects.get(email=fields['email']):
            return {'is_new': False, 'user': User.objects.get(email=fields['email'])}
    except:
        pass
    if not fields:
        return

    user = strategy.create_user(**fields)
    return {
        'is_new': True,
        'user': user
    }


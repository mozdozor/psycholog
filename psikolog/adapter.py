import json
import base64
import logging

from django.core.exceptions import FieldDoesNotExist
from django.db.models import  FileField
from django.db.models.fields import (BinaryField)
from django.utils import six
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import HttpResponse, redirect



from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from allauth.utils import SERIALIZED_DB_FIELD_PREFIX
from allauth.exceptions import ImmediateHttpResponse



from psikolog.models import CustomUserModel
logger = logging.getLogger("django")





class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    """Custom SocialAccountAdapter for django-allauth.
    Replaced standard behavior for serialization of TimeZoneField.

    Need set it in project settings:
    SOCIALACCOUNT_ADAPTER = 'myapp.adapter.MySocialAccountAdapter'
    """

    def __init__(self, request=None):
        super(MySocialAccountAdapter, self).__init__(request=request)

    def pre_social_login(self, request, sociallogin):
        # This isn't tested, but should work
        try:
            emails = [email.email for email in sociallogin.email_addresses]
            user = CustomUserModel.objects.get(email__in=emails)
            sociallogin.connect(request, user)
            raise ImmediateHttpResponse(response=HttpResponse())
        except CustomUserModel.DoesNotExist:
            user=sociallogin.user
            user.username=user.email
            user.save()
            sociallogin.connect(request, user)
            return redirect("index")
        except Exception as ex:
            logger.error(ex)

 
from twilio.rest import Client
import random
import math
import re
import environ
env = environ.Env()
environ.Env.read_env()
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

PHONE_REGEX = r"(^923[0-9]{9})"

def generate_otp():
    digits = [i for i in range(0, 10)]
    otp = ""
    for i in range(6):
        index = math.floor(random.random() * 10)
        otp += str(digits[index])
    return otp


def send_otp(phone):
    try:
        account_sid = env('TWILIO_ACCOUNT_SID')
        auth_token = env('TWILIO_AUTH_TOKEN')
        client = Client(account_sid, auth_token)
        otp = generate_otp()
        message = client.messages.create(
                                body= f'Hi! Your OTP is [{otp}], please verify your phone number',
                                from_='+19706458878',
                                to='+'+ phone)
    except:
        # In case if trial account does not work (because of expiry)
        otp = "123456"
    return otp



def password_is_valid(password, confirm_password):
    """Validates that a password is as least 7 characters long and has at least
    1 digit and 1 letter.
    """
    min_length = 8

    if password != confirm_password:
        return False

    if len(password) < min_length:
        return False


    if not any(char.isdigit() for char in password):
        return False


    if not any(char.isalpha() for char in password):
        return False

    return True


def delete_session(request):
    request.session.get('otp', None)
    request.session.get('first_name', None)
    request.session.get('last_name', None)
    request.session.get('password', None)
    request.session.get('phone', None)


def validate_phone(phone):
    try:
        """
        formats the mobile number in correct form
        """
        if phone and not re.fullmatch(PHONE_REGEX, phone):
            return False
        else:
            return True
    except:
        raise ValidationError(_('Please try again'))








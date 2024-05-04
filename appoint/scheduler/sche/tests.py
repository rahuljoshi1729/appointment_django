from django.test import TestCase
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

# Create your tests here.
import hashlib
import hmac
import base64

""" Hash-based message authentication code (or HMAC) is a cryptographic authentication technique that uses a hash function and a secret key.
With HMAC, you can achieve authentication and verify that data is correct and authentic with shared secrets, as opposed to approaches that use signatures and asymmetric cryptography. """



def create_token(user,salt):
    token=AccessToken.for_user(user)
    return str(token)


def decode_token(token):
    try:
        token_obj = AccessToken(token)
        user_id = token_obj.payload['user_id']
        return user_id
    except InvalidToken:
        # Token is invalid or expired
        return None
    except TokenError:
        # Other token decoding errors
        return None
        
    
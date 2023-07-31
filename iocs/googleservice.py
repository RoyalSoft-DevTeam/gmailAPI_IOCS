import requests

from django.conf import settings
from typing import Dict, Any
from django.core.exceptions import ValidationError

GOOGLE_ID_TOKEN_INFO_URL = 'https://www.googleapis.com/oauth2/v3/tokeninfo'
GOOGLE_ACCESS_TOKEN_OBTAIN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_USER_INFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'


def exchange_code(auth_code: str) -> str:

    data = {
        'code': auth_code,
        'client_id': settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['client_id'],
        'client_secret': settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['secret'],
        'redirect_uri': 'postmessage',
        'grant_type': 'authorization_code'
    }

    response = requests.post(GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=data)

    return response.json()['access_token']
    # return JsonResponse(response.json(), status=200)
def google_get_user_info(*, access_token: str) -> Dict[str, Any]:
    # Reference: https://developers.google.com/identity/protocols/oauth2/web-server#callinganapi
    response = requests.get(
        GOOGLE_USER_INFO_URL,
        params={'access_token': access_token}
    )

    if not response.ok:
        raise ValidationError('Failed to obtain user info from Google.')

    return response.json()
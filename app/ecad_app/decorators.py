from decouple import config
from functools import wraps
from django.conf import settings
from django.utils.http import urlencode
from django.contrib import messages
import requests, urllib, urllib.parse, json


def check_recaptcha(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        request.recaptcha_is_valid = None
        # recaptcha_response = None
        if request.method == 'POST':
            if request.POST.get('action') == 'newCmt_Form' or request.POST.get('action') == 'sendCtct_Form':
                recaptcha_response = request.POST.get('grecaptcha_response')
                print('\n\n# --- PY: decorator is working! trying to verify captcha... --- #')
                url = 'https://www.google.com/recaptcha/api/siteverify'
                values = {
                    'secret': config('GOOGLE_RECAPTCHA_SECRET_KEY'),
                    'response': recaptcha_response
                }
                print(f'\n\n# --- PY: processing captcha... --- #')
                data = urllib.parse.urlencode(values).encode()
                req =  urllib.request.Request(url, data=data)
                response = urllib.request.urlopen(req)
                result = json.loads(response.read().decode())     
                print(f'\n\n# --- PY: Captcha processed with the following values: --- #\n{values}')

                print(f'\n\n# --- PY: Captcha result: --- # \n{result}')
                if result['success']:
                    request.recaptcha_is_valid = True
                else:
                    request.recaptcha_is_valid = False
                    print('\n\n# --- PY: Captcha failed --- #')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
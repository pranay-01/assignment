from cryptography.fernet import Fernet
from django.utils.deprecation import MiddlewareMixin
from engines.settings import KEY
import json

# Yet to complete
class CustomMiddleware(MiddlewareMixin):

    def process_request(self, request):

        if request.method == 'POST':
            kf = Fernet(KEY)
           # print(request.META['CONTENT_TYPE'])
            data = request.body
            print('Middleware for post requests')
            #enc = kf.encrypt(data)
            #print(enc)

        if request.method == 'GET':
            print('Middleware for get requests')

        return None
'''
    def process_response(self, request, response):

        print(response)
        return response
'''
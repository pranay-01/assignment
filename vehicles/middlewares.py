from cryptography.fernet import Fernet
from django.utils.deprecation import MiddlewareMixin
from engines.settings import KEY
import json

# Yet to complete
class CustomMiddleware(MiddlewareMixin):

    def process_request(self, request):

        WHITE_LIST = [
            "/vehicles/",
            "/vehicles/displayplaces/"
        ]

        if request.method == 'POST' and request.path in WHITE_LIST:
            kf = Fernet(KEY)
           # print(request.META['CONTENT_TYPE'])
            data = request.POST
            print(request.POST.get("area"))
            #enc = kf.encrypt(data)
            #print(enc)

        if request.method == 'GET':
            if request.path in WHITE_LIST:
                print(request.path + "  this is the path")
            else:
                print("no not you")
        return None
'''
    def process_response(self, request, response):

        print(response)
        return response
'''
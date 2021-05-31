
from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response
import json

key = 7

WHITE_LIST = [
    "/demos/middleware/",
]

class CustomTop(MiddlewareMixin):

    def process_request(self, request):

        if request.method == 'POST' and request.path in WHITE_LIST:

            mesg = request.POST.get('codeword')
            print(mesg)
            request.POST = request.POST.copy()
            enc = ""
            for i in range(len(mesg)):
                each = mesg[i]

                if (each.isupper()):
                    enc += chr((ord(each) + key - 65) % 26 + 65)
                else:
                    enc += chr((ord(each) + key - 97) % 26 + 97)

            request.POST['codeword']= enc

        return None


    def process_response(self, request, response):


            mesg = ""
            enc = response.data['Mesg']
            for i in range(len(enc)):
                each = enc[i]
                if (each.isupper()):
                    mesg += chr((ord(each) - key - 65) % 26 + 65)
                else:
                    mesg += chr((ord(each) - key - 97) % 26 + 97)
                response.data['Mesg'] = mesg
            print(mesg)
            return response



class CustomMiddle(MiddlewareMixin):

    def process_request(self, request):

        if request.method == 'POST' and request.path in WHITE_LIST:

            print('-------------------------MIDDLEWARE(REQUEST-CYCLE)-------------------- '+ request.POST.get('codeword'))

        return None

    def process_response(self, request, response):

            print('--------------------------MIDDLEWARE(RESPONSE-CYCLE)------------------- '+   response.data['Mesg'])
            return response



class CustomBottom(MiddlewareMixin):

    def process_request(self, request):

        if request.method == 'POST' and request.path in WHITE_LIST:
            enc = request.POST.get('codeword')
            request.POST = request.POST.copy()
            mesg = ""
            for i in range(len(enc)):
                each = enc[i]

                if (each.isupper()):
                    mesg += chr((ord(each) - key - 65) % 26 + 65)

                else:
                    mesg += chr((ord(each) - key - 97) % 26 + 97)
            request.POST['codeword']=mesg
            print(mesg)

        return None

    def process_response(self, request, response):

            mesg = response.data['Mesg']
            print(mesg)
            enc = ""
            for i in range(len(mesg)):
                each = mesg[i]

                if (each.isupper()):
                    enc += chr((ord(each) + key - 65) % 26 + 65)

                else:
                    enc += chr((ord(each) + key - 97) % 26 + 97)
            response.data['Mesg'] = enc
            return response
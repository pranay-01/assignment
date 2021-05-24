from django.shortcuts import render
from .models import Bank, Sample, DemoModel, FileUpload
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.views.decorators.csrf import csrf_exempt
from .serializers import SampleSerializer, DemoModelSerializer, FileUploadSerializer
from django.utils.crypto import get_random_string
from django.db.models.signals import post_delete
from django.db import connection
import time, base64
from django.core.files.storage import FileSystemStorage


#------------------------------------FILE UPLOAD-------------------------#

def SimpleUpload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        FileUpload.objects.create(file=uploaded_file_url)
        return render(request, 'fileupload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'fileupload.html')


class UploadView(APIView):

    def post(self, request):

        byte = request.data['encoded']
        bytess = byte.encode('utf-8')
        decodeit = open('media/dummmy_back.txt', 'wb')
        decodeit.write(base64.b64decode((bytess)))
        decodeit.close()
        return Response({
            'Mesg': 'Got Back the Information'
        })

#---------------CSRF-------------------------#

@csrf_exempt
def Formview(request):

    if request.POST.get('acc') and request.POST.get('money'):
        bank = Bank()
        bank.acc_name = request.POST.get('accn')
        bank.acc_no = request.POST.get('acc')
        bank.money = request.POST.get('money')
        bank.save()

    return render(request, 'form.html')


def Autoview(request):

    return render(request, 'autoform.html')

def Auto_send(request):
        acc_name = request.POST.get('acc_name', None)
        acc_no = request.POST.get('acc_no', None)
        money = request.POST.get('money', None)
        Bank.objects.create(acc_name=acc_name, acc_no=acc_no, money=money)

        return HttpResponse(status=201)


#-----------------------MiDDLEWARE------------------------------#


class SampleView(APIView):
    def get(self, request, format=None):

        return Response({'Mesg': 'GET'})

    def post(self,request):

        return Response({'Mesg': 'darknight'})



#----------------------------ORM Scenarios--------------------------------#

class ScenarioFour(APIView):

    def get(self, request, format=None):

        l=[]
        for i in range(1000):
            l.append(get_random_string(5, allowed_chars='pranay'))

        entries = [DemoModel(txt=val) for val in l]

        DemoModel.objects.bulk_create(entries)

        return Response({'mesg': 'Created Random Entries'})


class ScenarioFive(APIView):

    def get(self,request, format=None):

        return Response({'mesg': 'GET'})

    def post(self, request):

        keys = request.data['key']
        flag=0
        start= time.time()
        for each in Sample.objects.all().iterator():
            if each.exp in keys:
                flag+=1
        end= time.time()
        diff = end-start
        return Response({'Matching Rows': flag,
                         'time': diff})


class ScenarioNine(APIView):

    def get(self, request, format=None):

        return Response({
            'mesg' : 'GET'
        })
    def post(self, request):

        keys = request.data['key']
        for i in range(len(keys)):
            if(len(keys[i]) == 2):
                temp = DemoModel.objects.get(id=keys[i]['id'])
                temp.txt = keys[i]['name']
                temp.save()
            else:
                DemoModel.objects.create(txt=keys[i]['name'])

        return Response({
            'Mesg': 'Random Creation and Updation'
        })


class ScenarioTen(APIView):

    def get(self, request, format=None):

        return Response({
            'Method': 'GET'
        })
    def post(self, request):

        keys = request.data['key']
        l=len(keys)
        mid=l//2
        f_half=[]
        s_half=[]
        f_half= keys[:mid]
        s_half=keys[mid:]
        #for each in f_half:
        if DemoModel.objects.filter(id=907).exists():
            x=DemoModel.objects.get(id=907)
            x.delete()


        return Response({
            'mesg': 'Intelligent Deletion'
        })




#--------------------------------TESTING-------------------------#

'''
class Example(APIView):

    def get(self, request, format=None):

        for each in Bank.objects.all():
            print(each.money)

        return Response({
            "sql": len(connection.queries)
        })
'''


class Example(APIView):


    def get(self, request, format=None):

        return Response({'mesg': 'Get'})

    def post(self, request, format=None):

        l = request.data['key']

        return Response({'mesg': request.data['name'],
                        'info': l[0]})
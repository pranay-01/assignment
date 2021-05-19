from django.shortcuts import render
from .models import Bank
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .serializers import SampleSerializer

# Create your views here.


@csrf_exempt
def formview(request):

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


@api_view(['GET', 'POST'])
def SampleView(request):

       samp = SampleSerializer(data=request.data)

       return Response(samp.initial_data)

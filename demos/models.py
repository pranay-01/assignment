from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete



class Bank(models.Model):

    acc_name = models.CharField(max_length=25, default='Abc')
    acc_no = models.IntegerField()
    money = models.IntegerField()

    def __str__(self):
        return self.acc_name


class Sample(models.Model):

    exp = models.CharField(max_length=150)

    def __str__(self):
        return self.exp


class DemoModel(models.Model):

    txt = models.CharField(max_length=150)

    class Meta:
        indexes = [models.Index(fields=['txt', ])]

    def __str__(self):
        return self.txt

    def del_mesg(sender, **kwargs):
        print('Deletion done, You are from Second half')


post_delete.connect(sender=DemoModel, receiver=DemoModel.del_mesg)



class FileUpload(models.Model):
    file = models.FileField(upload_to='media/')




'''
    class Meta:
        indexes =[ models.Index(fields=['exp'])
        ]
'''
from django.db import models
# Create your models here.


class Bank(models.Model):

    acc_name = models.CharField(max_length=25, default='Abc')
    acc_no = models.IntegerField()
    money = models.IntegerField()

    def __str__(self):
        return self.acc_name
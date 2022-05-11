# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from goods.models import *
from userapp.models import UserInfo


class CartItem(models.Model):
    goodsid = models.PositiveIntegerField()
    colorid = models.PositiveIntegerField()
    sizeid = models.PositiveIntegerField()
    count = models.PositiveIntegerField()
    isdelete = models.BooleanField(default=False)
    user = models.ForeignKey(UserInfo,on_delete=models.CASCADE)


    class Meta:
        unique_together = ['goodsid','colorid','sizeid']

    def getGoods(self):
        return Goods.objects.get(id=self.goodsid)

    def getColor(self):
        return Color.objects.get(id=self.colorid)

    def getSize(self):
        return Size.objects.get(id=self.sizeid)

    def getTotalPrice(self):
        import math
        return math.ceil(float(self.getGoods().price) * int(self.count))













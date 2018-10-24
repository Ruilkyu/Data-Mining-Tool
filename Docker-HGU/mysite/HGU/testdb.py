from django.http import HttpResponse
from .models import hguTest


def testHguDB(request):
    s = hguTest(name="pointToPoint", ip="192.168.1.34")
    s.save()
    # s1 = hguTest.objects.get(id = 1)
    # s1.delete()
    return HttpResponse("<h>一条数据添加成功</h>")

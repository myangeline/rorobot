import datetime
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from utils.mongodbutil import get_db


def index(request):
    # return HttpResponse('Hello')
    return render(request, 'article/../../templates/base.html')


def category(request):
    db = get_db()
    results = db.category.find().sort([("create_date", 1)])
    return render(request, 'article/category.html', locals())


def publish(request):
    return render(request, 'article/publish.html', locals())


def manage(request):
    return render(request, 'article/manage.html', locals())


@csrf_exempt
def add_category(request):
    category_name = request.POST.get('textCategoryName', None)
    if category_name:
        db = get_db()
        doc = {
            'name': category_name,
            'total': 0,
            'create_date': datetime.datetime.now()
        }
        db.category.insert_one(doc)
    return HttpResponseRedirect('/admin/category/')


@csrf_exempt
def check_category_name(request):
    name = request.POST.get('name', None)
    if name:
        db = get_db()
        result = db.category.find_one({'name': name})
        if result:
            return HttpResponse(json.dumps({'status': 0, 'msg': '<span style="color: red;">类别名称已存在！</span>'}))
        else:
            return HttpResponse(json.dumps({'status': 1, 'msg': '<span style="color: green;">类别名称可用！</span>'}))
    else:
        return HttpResponse(json.dumps({'status': 0, 'msg': '<span style="color: red;">类别名称不能为空！</span>'}))
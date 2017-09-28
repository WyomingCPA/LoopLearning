from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404

from .models import Lesson, Category, TodayCount
from django.db.models import Avg, Max, Min

from datetime import datetime, timedelta
import time

from xml.etree.ElementTree import fromstring, ElementTree

import random

@login_required(login_url='/admin/')
def index(request):
    category = Category.objects.all()
    day = time.strftime("%Y-%m-%d")
    try:
        day_count = TodayCount.objects.filter(day__istartswith=day).first().count
    except:
        day_count = 0

    return render(request, 'Learning/index.html', {'day_count': day_count, 'category' : category })

@login_required(login_url='/admin/')
def random_learn(request, slug):
    category = Category.objects.get(name = slug)
    lesson = list(Lesson.objects.filter(category = category).values())

    random.shuffle(lesson)
    lesson_srez = lesson[:10]
    min_val = min(lesson_srez, key=lambda x:x['count'])

    return render(request, 'Learning/random_learn.html', {'lesson': min_val })

def action(request):

    if 'i_read' in request.POST:
        id = request.POST.getlist('i_read')
        lesson = Lesson.objects.get(id=int(id[0]))
        lesson.time_update = datetime.now()
        lesson.count = lesson.count + 1
        lesson.save()

        day = time.strftime("%Y-%m-%d")

        amount_day_filter = TodayCount.objects.filter(day__istartswith=day).first()
        if (amount_day_filter != None):       
            amount_day_filter.count =  amount_day_filter.count + 1
            amount_day_filter.save()
            return redirect('/')
        else:
            amount_day_new = TodayCount()
            amount_day_new.save()
            return redirect('/')

    if 'delete' in request.POST:
        id = request.POST.getlist('delete')
        lesson = Lesson.objects.get(id=int(id[0]))
        lesson.delete()

        return redirect('/')

    return render(request, 'Learning/index.html', )


def add_learn_form(request):

     return render(request, 'Learning/forms_learn.html', )

def add_learn_form_action(request):
    if request.method == "POST":
        my_uploaded_file = request.FILES['my_uploaded_file'].read()

        tree = ElementTree(fromstring(my_uploaded_file))
        root = tree.getroot()
        for child_of_root in root.findall('link'):
            category = child_of_root.find('category').text
            link = child_of_root.find('link').text
            title = child_of_root.find('title').text

            category_model = Category.objects.get(name = category)
            try:
               Lesson.objects.get(url=link)
            except Lesson.MultipleObjectsReturned:
                pass
            except Lesson.DoesNotExist:                                             
                itemLearn = Lesson(category = category_model, title = title, url = link)
                itemLearn.save()

        return redirect('/')
    else:
        return redirect('/')

    return render(request, 'Learning/forms_learn.html', )
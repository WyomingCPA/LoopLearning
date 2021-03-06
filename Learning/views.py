from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.utils import timezone
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
    day = timezone.datetime.now().strftime("%Y-%m-%d")
    try:
        day_count = TodayCount.objects.filter(day__istartswith=day).first().count
    except:
        day_count = 0

    return render(request, 'Learning/index.html', {'day_count': day_count, 'category' : category })


@login_required(login_url='/admin/')
def list_index(request):
    category = Category.objects.all()
    return render(request, 'Learning/list_index.html', {'category' : category })

@login_required(login_url='/admin/')
def list_table(request, slug):
    category = Category.objects.get(name = slug)
    lesson = Lesson.objects.filter(category = category).values().order_by('time_update')

    paginator = Paginator(lesson, 50)
    page = request.GET.get('page')
    try:
        lesson = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        lesson = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        lesson = paginator.page(paginator.num_pages)


    return render(request, 'Learning/list_table.html', {'lesson' : lesson })


@login_required(login_url='/admin/')
def random_learn(request, slug):
    category = Category.objects.get(name = slug)
    lesson = list(Lesson.objects.filter(category = category).values())

    random.shuffle(lesson)
    min_val = min(lesson, key=lambda x:x['count'])

    return render(request, 'Learning/random_learn.html', {'lesson': min_val })

@login_required(login_url='/admin/')
def random_repeat_learn(request, slug):
    category = Category.objects.get(name = slug)
    lesson = list(Lesson.objects.filter(category = category, count__gt = 0,).values().order_by('time_update')[0:5])

    random.shuffle(lesson)
    min_val = min(lesson, key=lambda x:x['count'])

    return render(request, 'Learning/random_repeat_learn.html', {'lesson': min_val })

@login_required(login_url='/admin/')
def random_list_category(request):
    category = Category.objects.all()
    return render(request, 'Learning/random.html', { 'category' : category })

@login_required(login_url='/admin/')
def random_list_repeat_category(request):
    category = Category.objects.all()
    return render(request, 'Learning/random_repeat_category.html', { 'category' : category })

@login_required(login_url='/admin/')
def statistic_category(request):
    category = Category.objects.all()

    learn_compleated_category = []

    for item_category in category:
        lesson = list(Lesson.objects.filter(category = item_category).values())
        count_all_category = len(lesson)
        count_compleated_category = 0
        for item_lesson in lesson:
            if (item_lesson['count'] != 0):
                count_compleated_category += 1

        learn_compleated_item = {'category' : item_category.name, 'count_all_category' : count_all_category, 'count_compleated_category' : count_compleated_category}
        learn_compleated_category.append(learn_compleated_item)
    
    severn_day_count = TodayCount.objects.all().values().order_by('-day')[:30]
            
    return render(request, 'Learning/statistic.html', {'learn_compleated_category': learn_compleated_category, 'severn_day_count': severn_day_count })

def action(request):

    if 'i_read' in request.POST:
        id = request.POST.getlist('i_read')
        lesson = Lesson.objects.get(id=int(id[0]))
        lesson.time_update = timezone.datetime.now()
        lesson.count = lesson.count + 1
        lesson.save()

        day = datetime.now().strftime("%Y-%m-%d")

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

def action_repeat(request):

    if 'i_read' in request.POST:
        id = request.POST.getlist('i_read')
        lesson = Lesson.objects.get(id=int(id[0]))
        lesson.time_update = timezone.datetime.now()
        lesson.count = lesson.count + 1
        lesson.save()

        day = datetime.now().strftime("%Y-%m-%d")

        amount_day_filter = TodayCount.objects.filter(day__istartswith=day).first()
        if (amount_day_filter != None):       
            amount_day_filter.count =  amount_day_filter.count + 1
            amount_day_filter.save()
            return redirect('/random/repeat/category/')
        else:
            amount_day_new = TodayCount()
            amount_day_new.save()
            return redirect('/random/repeat/category/')

    if 'delete' in request.POST:
        id = request.POST.getlist('delete')
        lesson = Lesson.objects.get(id=int(id[0]))
        lesson.delete()

        return redirect('/random/repeat/category/')

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


@login_required(login_url='/admin/')
def action_learn_table(request):
    if request.method == 'POST':
        pointer_lesson = request.POST.getlist('pointer_lesson[]')
        for item in pointer_lesson:
            lesson = Lesson.objects.get(id=int(item))
            lesson.time_update = timezone.datetime.now()
            lesson.count = lesson.count + 1
            lesson.save()
            
            day = timezone.datetime.now().strftime("%Y-%m-%d")
            amount_day_filter = TodayCount.objects.filter(day__istartswith=day).first()
            if (amount_day_filter != None):       
                amount_day_filter.count =  amount_day_filter.count + 1
                amount_day_filter.save()
                return redirect('/list/')
            else:
                amount_day_new = TodayCount()
                amount_day_new.save()
                return redirect('/list/')            

    return redirect('/list/')
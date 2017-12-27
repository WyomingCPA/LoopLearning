from django.contrib import admin
from django.utils import timezone

from Learning.models import Category, Lesson, TodayCount

from datetime import timedelta
import time

def make_published(modeladmin, request, queryset):
    for obj in queryset:
        obj.time_update = timezone.datetime.now()
        obj.count = obj.count + 1
        obj.save()

        #day = time.strftime("%Y-%m-%d")
        day = timezone.datetime.now().strftime("%Y-%m-%d")

        amount_day_filter = TodayCount.objects.filter(day__istartswith=day).first()
        if (amount_day_filter != None):       
            amount_day_filter.count =  amount_day_filter.count + 1
            amount_day_filter.save()
            
        else:
            amount_day_new = TodayCount()
            amount_day_new.save()
         




make_published.short_description = "Read"


class LessonAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ('title', 'category', 'show_lesson_url', 'time_update', 'count')
    list_filter = ('category', 'count', )
    actions = [make_published]

    def show_lesson_url(self, obj):
        return '<a href="%s" target="_blank">%s</a>' % (obj.url, obj.url)

    show_lesson_url.allow_tags = True
admin.site.register(Category)
admin.site.register(Lesson, LessonAdmin)
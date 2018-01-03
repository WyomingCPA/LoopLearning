from django.contrib import admin
from django.utils import timezone
from django.core.urlresolvers import reverse

from django.templatetags.static import static

from Learning.models import Category, Lesson, TodayCount

from tinymce.widgets import TinyMCE

from datetime import timedelta
import time
        
class LessonAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ('title', 'category', 'show_lesson_url', 'show_lesson_resume','time_update', 'count')
    list_filter = ('category', 'count', )
    actions = ['make_published']

    item_row = 1


    class Media:
        #from django.conf import settings
        #media_url = getattr(settings, 'MEDIA_URL', '/media')
        #js = [ media_url+'admin/my.js', ]
        css = {'all': ('//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css',) }
        js = ['https://code.jquery.com/jquery-1.12.4.js', 'https://code.jquery.com/ui/1.12.1/jquery-ui.js', static('Learning/admin/my.js')]


    def show_lesson_url(self, obj):
        return '<a href="%s" target="_blank">%s</a>' % (obj.url, obj.url)

    def show_lesson_resume(self, obj):
        if (len(obj.resume) != 0):
            dialog = '<a href="#" id="opener-%s" >resume-%s</a><div id="dialog-%s" title="resume" style="float:left; margin:0 7px 50px 0;display:none;">%s</div>' % (self.item_row, self.item_row, self.item_row, obj.resume)
            self.item_row += 1
            return dialog 

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

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'resume':
            return db_field.formfield(widget=TinyMCE(
                attrs={'cols': 200, 'rows': 100, },
                mce_attrs={'external_link_list_url': reverse('tinymce-linklist')},
            ))
        return super(LessonAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    show_lesson_url.allow_tags = True
    show_lesson_resume.allow_tags = True
    make_published.short_description = "Read"

admin.site.register(Category)
admin.site.register(Lesson, LessonAdmin)
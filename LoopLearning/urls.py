from datetime import datetime
from django.contrib import admin
from django.conf.urls import url, include
import django.contrib.auth.views
from Learning.views import index, list_table, list_index, random_learn, action, add_learn_form, add_learn_form_action, action_learn_table, statistic_category, random_list_category, random_list_repeat_category, random_repeat_learn, action_repeat

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index, name='index'),
    url(r'^random/category/(?P<slug>[\w-]+)/', random_learn, name='random_learn'),
    url(r'^random/repeat/category/(?P<slug>[\w-]+)/', random_repeat_learn, name='random_repeat_learn'),
    url(r'^random/category/', random_list_category, name='random_list_category'),
    url(r'^random/repeat/category/', random_list_repeat_category, name='random_list_repeat_category'),
    url(r'^list/(?P<slug>[\w-]+)/', list_table, name='list_table'),
    url(r'^list/', list_index, name='list_index'),
    url(r'^statistic/', statistic_category, name='statistic_category'),
    url(r'^action/', action, name='action'),
    url(r'^action_repeat/', action_repeat, name='action_repeat'), 
    url(r'^add_learn/', add_learn_form, name = 'add_learn_form'),
    url(r'^add_learn_action/', add_learn_form_action, name = 'add_learn_form_action'),
    url(r'^action_learn_table/', action_learn_table, name = 'action_learn_table'),
]

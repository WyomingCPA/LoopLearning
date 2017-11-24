from datetime import datetime
from django.contrib import admin
from django.conf.urls import url, include
import django.contrib.auth.views

from Learning.views import index, list_table, list_index, random_learn, action, add_learn_form, add_learn_form_action, action_learn_table, statistic_category

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index, name='index'),
    url(r'^category/(?P<slug>[\w-]+)/', random_learn, name='random_learn'),
    url(r'^list/(?P<slug>[\w-]+)/', list_table, name='list_table'),
    url(r'^list/', list_index, name='list_index'),
    url(r'^statistic/', statistic_category, name='statistic_category'),
    url(r'^action/', action, name='action'),
    url(r'^add_learn/', add_learn_form, name = 'add_learn_form'),
    url(r'^add_learn_action/', add_learn_form_action, name = 'add_learn_form_action'),
    url(r'^action_learn_table/', action_learn_table, name = 'action_learn_table')
]

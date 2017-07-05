from datetime import datetime
from django.contrib import admin
from django.conf.urls import url, include
import django.contrib.auth.views

from Learning.views import index, random_learn, action, add_learn_form, add_learn_form_action

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index, name='index'),
    url(r'^category/(?P<slug>[\w-]+)/', random_learn, name='random_learn'),
    url(r'^action/', action, name='action'),
    url(r'^add_learn/', add_learn_form, name = 'add_learn_form'),
    url(r'^add_learn_action/', add_learn_form_action, name = 'add_learn_form_action')
]

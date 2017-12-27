from django.db import models



class Lesson(models.Model):
    title = models.CharField(max_length=300)
    resume = models.TextField(blank=True)
    url = models.CharField(max_length=200)
    time_update = models.DateTimeField(null=True, blank=True)
    count = models.IntegerField(default = 0)
    category = models.ForeignKey('Category')

    def __unicode__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name

class TodayCount(models.Model):
    day = models.DateTimeField(auto_now = True)
    count = models.IntegerField(default = 0)


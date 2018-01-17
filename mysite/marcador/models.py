# encoding: utf-8
from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now


@python_2_unicode_compatible
class Schedule(models.Model):
    room_id = models.CharField(max_length=50)
    num_employee = models.IntegerField()
    date_time = models.DateField()

    class Meta:
        verbose_name = 'schedule'
        verbose_name_plural = 'schedules'
        ordering = ['room_id']

    def __str__(self):
        return "date: %s room id: %s " % (self.date_time, self.room_id)


@python_2_unicode_compatible
class Friend(models.Model):
    id = models.CharField(max_length=9, unique=True, primary_key=True)

    class Meta:
        verbose_name = 'friend'
        verbose_name_plural = 'friends'
        ordering = ['id']

    def __str__(self):
        return self.id


class PublicEmployeeManager(models.Manager):
    def get_queryset(self):
        qs = super(PublicEmployeeManager, self).get_queryset()
        return qs.filter()


@python_2_unicode_compatible
class Employee(models.Model):
    id = models.CharField('user id', primary_key=True, max_length=9)
    name = models.CharField('user name', max_length=255)
    access_permission = models.IntegerField('access_permission')
    role = models.CharField('role', max_length=255)
    friends = models.ManyToManyField(Friend, blank=True , related_name='friends')
    schedule = models.ManyToManyField(Schedule, blank=True)
    password = models.CharField('password', max_length=255)

    class Meta:
        verbose_name = 'employee'
        verbose_name_plural = 'employees'
        ordering = ['name']

    def __str__(self):
        return self.name

    objects = models.Manager()
    public = PublicEmployeeManager()

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .models import Employee


def friends_list(request):
    friends = Employee.public.all()
    context = {'friends': friends}
    return render(request, 'templates/marcador/friends_list.html', context)


def doors_user(request, username):
    user = get_object_or_404(User, username=username)
    # if request.user == user:
    #     friends = user.Employee.all()
    # else:
    #     friends = Employee.public.filter(owner__username=username)
    friends = Employee.public.filter(name=username)

    context = {'friends': friends, 'owner': user}
    return render(request, 'templates/marcador/doors_user.html', context)

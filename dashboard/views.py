from django.shortcuts import render, redirect


def index(request):
    return render(request, 'dashboard.html', {})

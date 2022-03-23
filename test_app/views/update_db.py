from django.shortcuts import render
from django.http import HttpResponseRedirect

from ..forms.modelForms import *


def update_db(request):
    return render(request, "test_app/update_db.html", {})

def type_sport(request):
    if request.method == 'POST':
        form = TypeOfSportForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

        return HttpResponseRedirect('/test/update_db/')
    else:
        form = TypeOfSportForm()
    return render(request, "test_app/form.html", {'form': form})

def book_dict(request):
    if request.method == 'POST':
        form = BookHoursDictForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

        return HttpResponseRedirect('/test/update_db/')
    else:
        form = BookHoursDictForm()
    return render(request, "test_app/form.html", {'form': form})

def kecamatan(request):
    if request.method == 'POST':
        form = KecamatanForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

        return HttpResponseRedirect('/test/update_db/')
    else:
        form = KecamatanForm()
    return render(request, "test_app/form.html", {'form': form})

def user_partner(request):
    if request.method == 'POST':
        form = UserPartnerForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

        return HttpResponseRedirect('/test/update_db/')
    else:
        form = UserPartnerForm()
    return render(request, "test_app/form.html", {'form': form})

def court(request):
    if request.method == 'POST':
        form = CourtForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

        return HttpResponseRedirect('/test/update_db/')
    else:
        form = CourtForm()
    return render(request, "test_app/form.html", {'form': form})

def article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

        return HttpResponseRedirect('/test/update_db/')
    else:
        form = ArticleForm()
    return render(request, "test_app/form.html", {'form': form})

def booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

        return HttpResponseRedirect('/test/update_db/')
    else:
        form = BookingForm()
    return render(request, "test_app/form.html", {'form': form})

def booking_hours(request):
    if request.method == 'POST':
        form = BookingHoursForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

        return HttpResponseRedirect('/test/update_db/')
    else:
        form = BookingHoursForm()
    return render(request, "test_app/form.html", {'form': form})
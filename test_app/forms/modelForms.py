from django import forms

from library.models.user import *
from library.models.court import *
from library.models.booking import *
from library.models.article import *


class TypeOfSportForm(forms.ModelForm):
    class Meta:
        model = TypeOfSport
        fields = '__all__'
        labels = {
        }

class BookHoursDictForm(forms.ModelForm):
    class Meta:
        model = BookHoursDict
        fields = '__all__'
        labels = {
        }
        widgets = {
        'hour_start': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        'hour_end': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        }

class KecamatanForm(forms.ModelForm):
    class Meta:
        model = KecamatanList
        fields = '__all__'
        labels = {
        }

class UserPartnerForm(forms.ModelForm):
    class Meta:
        model = UserPartner
        fields = '__all__'
        exclude = ['ts_created']
        labels = {
        }
        widgets = {
        }

class CourtForm(forms.ModelForm):
    class Meta:
        model = Court
        fields = '__all__'
        exclude = ['slug', 'ts_created', 'n_book']
        labels = {
        }

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
        exclude = ['data']
        labels = {
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'
        exclude = ['ts_created']
        labels = {
        }
        widgets = {
        'date_book': forms.DateInput(format=('%d-%m-%Y'), attrs={'type':'date'}),
        }

class BookingHoursForm(forms.ModelForm):
    class Meta:
        model = BookingHours
        fields = '__all__'
        exclude = []
        labels = {
        }
        
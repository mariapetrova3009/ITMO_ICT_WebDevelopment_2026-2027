from django import forms

from .models import Reservation, Review


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['check_in', 'check_out']

        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'}),
        }

class ReviewForm(forms.ModelForm):

    class Meta:

        model = Review
        fields = ['stay_from', 'stay_to', 'text', 'rating']
        widgets = {

            'stay_from': forms.DateInput(attrs={'type': 'date'}),
            'stay_to': forms.DateInput(attrs={'type': 'date'}),
            'text': forms.Textarea(attrs={'rows': 4}),
            'rating': forms.NumberInput(attrs={

                'min': 1,
                'max': 10,

            }),
        }
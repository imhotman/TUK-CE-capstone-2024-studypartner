from django import forms
from datetime import date


date = date.today()


class ForecastForm(forms.Form):
    year = forms.IntegerField(
        label='년도',
        min_value=date.year,
        widget=forms.NumberInput(attrs={
            'class': 'inputset-input form-control',
            'placeholder': 'Ex. 2025',
            'style': 'width: 50%;',
            'value': date.year,
        })
    )
    month = forms.ChoiceField(
        label='월',
        choices=[(str(i), f'{i}월') for i in range(1, 13) if i > date.month],
        widget=forms.Select(attrs={
            'class': 'inputset-input form-control',
            'style': 'width: 50%;',
        })
    )
    district = forms.CharField(
        label='구',
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'inputset-input form-control',
            'placeholder': 'Ex. 송파구',
            'style': 'width: 50%;',
        })
    )
    town = forms.CharField(
        label='동',
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'inputset-input form-control',
            'placeholder': 'Ex. 잠실2동',
            'style': 'width: 50%;',
        })
    )

# from django import forms
# from datetime import date


# date = date.today()


# class ForecastForm(forms.Form):
#     year = forms.IntegerField(
#         label='년도',
#         min_value=date.year,
#         widget=forms.NumberInput(attrs={
#             'class': 'inputset-input form-control',
#             'placeholder': 'Ex. 2025',
#             'style': 'width: 50%;',
#             'value': date.year,
#         })
#     )
#     month = forms.ChoiceField(
#         label='월',
#         choices=[(str(i), f'{i}월') for i in range(1, 13) if i > date.month],
#         widget=forms.Select(attrs={
#             'class': 'inputset-input form-control',
#             'style': 'width: 50%;',
#         })
#     )
#     district = forms.CharField(
#         label='구',
#         max_length=10,
#         widget=forms.TextInput(attrs={
#             'class': 'inputset-input form-control',
#             'placeholder': 'Ex. 송파구',
#             'style': 'width: 50%;',
#         })
#     )
#     town = forms.CharField(
#         label='동',
#         max_length=10,
#         widget=forms.TextInput(attrs={
#             'class': 'inputset-input form-control',
#             'placeholder': 'Ex. 잠실2동',
#             'style': 'width: 50%;',
#         })
#     )





from django import forms
from datetime import date

class ForecastForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.today = date.today()

    year = forms.IntegerField(
        label='년도',
        min_value=date.today().year,
        widget=forms.NumberInput(attrs={
            'class': 'inputset-input form-control',
            'placeholder': 'Ex. 2025',
            'style': 'width: 50%;',
            'value': date.today().year,
        })
    )

    month = forms.ChoiceField(
        label='월',
        choices=[(str(i), f'{i}월') for i in range(1, 13)],
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

    def clean(self):
        cleaned_data = super().clean()
        year = cleaned_data.get("year")
        month = cleaned_data.get("month")
        selected_date = date(year, int(month), 1)
        if selected_date <= self.today:
            raise forms.ValidationError("현재 날짜보다 예측 년도/월이 높아야 합니다.")
        return cleaned_data


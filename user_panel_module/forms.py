from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from account_module.models import User


class ChangePasswordForm(forms.Form):
    name = forms.CharField(label='نام', validators=[validators.MaxLengthValidator(100)], widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    current_password = forms.CharField(label='کلمه عبور فعلی', validators=[validators.MaxLengthValidator(100)],
                                       widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password = forms.CharField(label='کلمه عبور جدید', validators=[validators.MaxLengthValidator(100)],
                                   widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(label='تکرار کلمه عبور', validators=[validators.MaxLengthValidator(100)],
                                       widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_confirm_password(self):
        password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            return confirm_password
        raise ValidationError('تکرار کلمه عبور با کلمه عبور مغایرت دارد')


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'avatar', 'address', 'about_user', ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            }),
            'about_user': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'id': 'message'
            })
        }

        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'avatar': 'تصویر پروفایل',
            'address': 'آدرس',
            'about_user': 'درباره شخص',
        }


class WarrantyForm(forms.Form):
    code_validity = forms.CharField(label='کد گارانتی', validators=[validators.MaxLengthValidator(200)],
                                    widget=forms.TextInput(attrs={'class': 'form-control'}))
    detail = forms.CharField(label='اطلاعات اضافی', validators=[validators.MaxLengthValidator(400)],
                             widget=forms.TextInput({'class': 'form-control'}))

class DiscountForm(forms.Form):
    code_discount = forms.CharField(label='کد تخفیف', validators=[validators.MaxLengthValidator(200)],
                                    widget=forms.TextInput(attrs={'class': 'form-control'}))
    detail = forms.CharField(label='اطلاعات اضافی', validators=[validators.MaxLengthValidator(400)],
                             widget=forms.TextInput({'class': 'form-control'}))
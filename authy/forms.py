from django import forms
from django.core.exceptions import ValidationError
from authy.models import User


def UserForbbiden(value):

    list_forbibbiden = ['admin', 'auth', 'self','python', 'django',
        'user', 'authentification', 'exception', 'pass', ''
    ]
    if value in list_forbibbiden:
        raise ValidationError('This is a reserve word')

def UserInvalid(value):
    list_invalid = ['@', '#', '&', '*', '+','%',')','()', '(', '`', '~', '']

    if value in list_invalid:
        raise ValidationError("This is an invalid user. Don't user this caractere \n")

def user_unique_email(value):
    if User.objects.filter(email__iexist = value).exists():
        raise ValidationError('User whit this email already exist')


class SignUpForm(forms.ModelForm):
    password = forms.CharField(
        max_length=40, 
        min_length=6 , 
        widget=forms.PasswordInput(), 
        required=True
    )
    confirm_password = forms.CharField(
        max_length=40, 
        min_length=6, 
        widget=forms.PasswordInput(), 
        required=True
    )

    
    class Meta:
        model = User
        fields = ("email", "username",
            'password',"confirm_password"
        )


    def __int__(self, *args, **kwargs):
        super(SignUpForm, self).__int__(*args, **kwargs)
        self.fields['username'].validators.append(UserForbbiden)
        self.fields['username'].validators.append(UserInvalid)
        self.fields['email'].validators.append(user_unique_email)
    
    def clean(self, *args, **kwargs):
        super(SignUpForm, self).clean(*args, **kwargs)
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            self._error['password'] = self.error_class(
                ['password do not match. Please try again']
            )
        return self.cleaned_data
    

class ChangePassword(forms.ModelForm):
    id = forms.CharField(widget=forms.HiddenInput())
    old_password = forms.CharField(
        max_length=40, 
        min_length=6, 
        widget=forms.PasswordInput(), 
        required=True
    )
    new_password = forms.CharField(
       max_length=40, 
        min_length=6, 
        widget=forms.PasswordInput(), 
        required=True
    )
    confirm_password = forms.CharField(
        max_length=40, 
        min_length=6, 
        widget=forms.PasswordInput(), 
        required=True
    )
    class Meta:
        model = User
        fields = ('old_password', 'new_password', 'confirm_password')
    
    def clean(self, *args, **kwargs):
        super(ChangePassword, self).clean(*args, **kwargs)
        id = self.cleaned_data.get('id')
        old_password = self.cleaned_data.get('old_password')
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')

        user = User.objects.get(pk = id)
        if not user.check_password(old_password):
            self._error['old_password'] = self.error_class(['oldpassword do not match'])
        if new_password != confirm_password:
            self._error['new_password'] = self.error_class(['password do not match'])
        return self.cleaned_data


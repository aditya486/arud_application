from django import forms
from django.contrib.auth.models import User
from .models import Employee, OPTIONS, GENDER_CHOICES, count


class RegisterForm(forms.ModelForm):
    email = forms.EmailField()
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect)
    Address = forms.CharField(max_length=1024)
    Mobile_No = forms.CharField(max_length=11)
    Programming_Languages = forms.MultipleChoiceField(
        choices=OPTIONS, widget=forms.CheckboxSelectMultiple)
    Date_of_Birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm Password'}))
    Country = forms.ChoiceField(choices=count, widget=forms.RadioSelect)
    Image = forms.ImageField(required=False)
    File = forms.FileField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'gender', 'Address',
                  'Date_of_Birth', 'Mobile_No', 'password', 'password_confirm', 'Programming_Languages', 'Country', 'Image', 'File']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('.com'):
            raise forms.ValidationError("Only .com email addresses allowed")
        return email

    def clean_Mobile_No(self):
        Mobile_No = self.cleaned_data.get('Mobile_No')
        if len(Mobile_No) < 9:
            raise forms.ValidationError(
                "This is India! Enter a 10 digit number!!!")
        return Mobile_No

    def clean_Date_of_Birth(self):
        Date_of_Birth = self.cleaned_data.get("Date_of_Birth")
        if not '%m-%d-%Y':
            raise forms.ValidationError(
                "value has an invalid date format. It must be in YYYY-MM-DD format.")
        return Date_of_Birth

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if not password_confirm:
            raise forms.ValidationError("You must confirm your password")
        if password != password_confirm:
            raise forms.ValidationError("Your passwords do not match")
        return cleaned_data


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class UpdateForm(forms.ModelForm):
    email = forms.EmailField()
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect)
    Address = forms.CharField(max_length=1024)
    Mobile_No = forms.CharField(max_length=11)
    Programming_Languages = forms.MultipleChoiceField(
        choices=OPTIONS, widget=forms.CheckboxSelectMultiple)
    Date_of_Birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}))
    count = (
        ("india", "India"),
        ("out", "other")
    )
    Country = forms.ChoiceField(choices=count, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ['email', 'gender', 'Address',
                  'Date_of_Birth', 'Mobile_No', 'Programming_Languages', 'Country']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('.com'):
            raise forms.ValidationError("Only .com email addresses allowed")
        return email

    def clean_Mobile_No(self):
        Mobile_No = self.cleaned_data.get('Mobile_No')
        if len(Mobile_No) < 9:
            raise forms.ValidationError(
                "This is India! Enter a 10 digit number!!!")
        return Mobile_No

    def clean_Date_of_Birth(self):
        Date_of_Birth = self.cleaned_data.get("Date_of_Birth")
        if not '%m-%d-%Y':
            raise forms.ValidationError(
                "value has an invalid date format. It must be in YYYY-MM-DD format.")
        return Date_of_Birth


class PasswordResetForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['password', 'password_confirm']

    def clean(self):
        cleaned_data = super(PasswordResetForm, self).clean()
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if not password_confirm:
            raise forms.ValidationError("You must confirm your password")
        if password != password_confirm:
            raise forms.ValidationError("Your passwords do not match")
        return cleaned_data

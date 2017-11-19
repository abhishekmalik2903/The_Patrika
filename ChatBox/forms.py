from datetime import datetime

from django import forms

from chat.models import FriendMessage, Profile


def years_widgets():
    """ returns a list of years from the current year to 120 years in the past. """
    now = datetime.now()
    start = now.year
    end = now.year - 120
    years = []
    while start > end:
        years.append(start)
        start -= 1
    return years


def must_be_empty(value):
    """ raises a ValidationError if "value" has a value"""
    if value:
        raise forms.ValidationError('is not empty')


class ContactStaffForm(forms.ModelForm):
    """ Form to contact staff"""
    title = forms.ChoiceField(choices=(("Response", "Response"), ('Request', 'request'), ('Complaint', 'compliant'),
                                       ('Praise', 'praise'), ("Question", "question"), ('Job', 'job')))

    class Meta:
        model = FriendMessage
        fields = ["title", "message"]

    def clean(self):
        cleaned_data = super().clean()


class UpdatePasswordForm(forms.Form):
    """ Form to update password. Its part of the ProfileUpdateForm.
    Its just separated so that the rest of the form could be validated without the password changing """
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    verify_password = forms.CharField(max_length=20, required=False, label="Please verify your password",
                                      widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        verify_password = cleaned_data.get('verify_password')

        if password != verify_password:
            raise forms.ValidationError("You must enter the same password in both fields")


class ProfileUpdateForm(forms.ModelForm):
    """ Form for user to update his personal info. Includes everything besides the Password. """
    birthday = forms.DateField(widget=forms.SelectDateWidget(years=years_widgets()))
    class Meta:
        model = Profile
        fields = ["first_name", "last_name", "phone", "email", "birthday", "gender", "picture"]

        honeypot = forms.CharField(required=False,
                                   widget=forms.HiddenInput,
                                   label="leave empty",
                                   validators=[must_be_empty],
                                   )

        def clean(self):
            cleaned_data = super().clean()
            email = cleaned_data.get('email')
            username = cleaned_data.get('first_name') + " " + cleaned_data.get('last_name')
            birthday = cleaned_data.get('birthday')

            if username == "ChatBox staff" or username == "No One":
                raise forms.ValidationError("sorry that username is reserved to the ChatBox staff")

            if birthday > datetime.now().date():
                raise forms.ValidationError("This date has not yet happened!")


class ProfileForm(forms.ModelForm):
    """ Form to sign up a new user. """
    birthday = forms.DateField(widget=forms.SelectDateWidget(years=years_widgets()))
    class Meta:
        model = Profile
        fields = ["picture", "first_name", "last_name",
                  "birthday", "gender", "phone", "email"]
    verify_email = forms.EmailField(max_length=150, label="Verify your email address")
    password = forms.CharField(widget=forms.PasswordInput)
    verify_password = forms.CharField(max_length=20, label="Verify your password", widget=forms.PasswordInput)
    honeypot = forms.CharField(required=False,
                               widget=forms.HiddenInput,
                               label="leave empty",
                               validators=[must_be_empty],
                               )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        verify_email = cleaned_data.get('verify_email')
        password = cleaned_data.get('password')
        verify_password = cleaned_data.get('verify_password')
        username = cleaned_data.get('first_name') + " " + cleaned_data.get('last_name')
        birthday = cleaned_data.get('birthday')

        if email != verify_email:
            raise forms.ValidationError("You must enter the same email in both fields")

        if password != verify_password:
            raise forms.ValidationError("You must enter the same password in both fields")

        if username == "ChatBox staff" or username == "No One":
            raise forms.ValidationError("Sorry that username is reserved to the ChatBox staff")
        elif Profile.objects.filter(username=username).exists():
            raise forms.ValidationError("Your name and/or password is taken.")
        if birthday > datetime.now().date():
            raise forms.ValidationError("This date has not yet happened!")


class LoginForm(forms.Form):
    """ Form for user to login """
    name = forms.CharField(max_length=100, label="Full Name")
    email = forms.EmailField(max_length=254, label="Email")
    password = forms.CharField(widget=forms.PasswordInput)
    honeypot = forms.CharField(required=False,
                               widget=forms.HiddenInput,
                               label="leave empty",
                               validators=[must_be_empty],
                               )

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

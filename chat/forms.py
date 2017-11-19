from django import forms

from chat import models


def must_be_empty(value):
    """ raises a ValidationError if "value" has a value"""
    if value:
        raise forms.ValidationError('is not empty')


class ChatPostForm(forms.ModelForm):
    """ Form to post a new Post. Has all four elements: image, title, text and share """
    class Meta:
        model = models.Chat
        fields = ['image', 'title', 'text', 'share']

    honeypot = forms.CharField(required=False,
                               widget=forms.HiddenInput,
                               label="leave empty",
                               validators=[must_be_empty],
                               )

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        text = cleaned_data.get('text')

        if not image and not text:
            raise forms.ValidationError("You need to post an image or a text")


class CommentForm(forms.ModelForm):
    """ Form to post a comment or a post a send a Private Message. It only has a image and text. """
    class Meta:
        model = models.Chat
        fields = ['image', 'text']

    honeypot = forms.CharField(required=False,
                               widget=forms.HiddenInput,
                               label="leave empty",
                               validators=[must_be_empty],
                               )

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        text = cleaned_data.get('text')
        if not image and not text:
            raise forms.ValidationError("You need to post an image or a text")

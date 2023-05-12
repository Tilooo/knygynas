from django import forms
from .models import BookReview, Profile
from django.contrib.auth.models import User

class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ['content']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']

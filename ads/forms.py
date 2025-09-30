from django import forms
from .models import Ad, Complaint

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['category','city','title','description','price','status']

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Shikoyatingizni yozing...'})
        }
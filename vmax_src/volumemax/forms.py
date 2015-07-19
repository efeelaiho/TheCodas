from django import forms

class SearchForm(forms.Form) :
    q = forms.CharField(label='', max_length=100,widget=forms.TextInput(attrs={'placeholder': 'Search'}))
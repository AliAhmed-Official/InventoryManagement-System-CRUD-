from django import forms

class Supplier_Form(forms.Form):
    Name = forms.CharField(label='Sup Name', widget=forms.TextInput(attrs={'class':'form-control'}))
    Contact = forms.CharField(label='Sup Contact', widget=forms.TextInput(attrs={'class':'form-control'}))
    Description = forms.CharField(label='Sup Description', widget=forms.Textarea(attrs={'class':'form-control'}))

class Category_Form(forms.Form):
    Category_Name = forms.CharField(label='Category Name', widget=forms.TextInput(attrs={'class':'form-control'}))

class Customer_Form(forms.Form):
    Name = forms.CharField(label='Customer Name', widget=forms.TextInput(attrs={'class':'form-control'}))
    Contact = forms.CharField(label='Customer Contact', widget=forms.TextInput(attrs={'class':'form-control'}))
    Address = forms.CharField(label='Customer Address', widget=forms.TextInput(attrs={'class':'form-control'}))
    Email = forms.CharField(label='Email Address', widget=forms.TextInput(attrs={'class':'form-control'}))
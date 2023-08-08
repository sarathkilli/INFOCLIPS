from django import forms


class UrlForm(forms.Form):

    url = forms.CharField(
        required=False, 
        label="Enter Url",
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 300px',"placeholder": "Enter the youtube url..."})
    )

    


class SearchForm(forms.Form):

    search = forms.CharField(
        required=False ,
        label="Search Term",
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 200px',"placeholder": "Enter the word to search..."})
    )
    

class TextForm(forms.Form):
    text = forms.CharField(
        label=None,
        widget=forms.Textarea(attrs={"rows":5, "cols":60, "style": "resize:none;","placeholder": "Enter text"}))


from cProfile import label
from django import forms

class TickerForm(forms.Form):
    ticker = forms.CharField( label='',widget=forms.TextInput(attrs={ 'placeholder': 'Enter stock symbol',
    'style': 'width:100%; height:1.5em; border: none; border-radius:10px 10px 10px 10px; background-color: white;color: #1C1B1B;font-size: 20px;padding-left: 5%;font-family: Roboto;'
    }))
    # ticker = forms.CharField(label='Ticker', max_length=5, widget=forms.TextInput(attrs={'placeholder': 'Enter ticker'}))

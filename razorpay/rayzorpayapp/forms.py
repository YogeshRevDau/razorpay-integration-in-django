from django import forms
from  .models import Order
class OrderForm(forms.ModelForm):
    class Meta:
        model= Order
        fields='__all__'
    # def __init__(self, *args, **kwargs):
    #     super(OrderForm, self).__init__(*args, **kwargs)
    #     for field in self.fields:
    #         self.fields['name'].widget.attrs['class'] = 'form-control'
    #         self.fields['amount'].widget.attrs['class'] = 'form-control'
    #         self.fields['services'].widget.attrs['class'] = 'form-control'
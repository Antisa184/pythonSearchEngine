# listings/forms.py
from django import forms

from .models import TextRecord

class RecordForm(forms.ModelForm):
   class Meta:
      model = TextRecord
      fields = '__all__'
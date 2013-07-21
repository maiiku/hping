# -*- coding: utf-8 -*-
from django import forms
from apps.pinger.models import Haystack
from apps.util.forms import BootstrapErrorList


class HaystackCreateModelForm(forms.ModelForm):
    error_class=BootstrapErrorList

    def __init__(self, *args, **kwargs):
        super(HaystackCreateModelForm, self).__init__(*args, **kwargs)
        self.error_class=BootstrapErrorList

    class Meta:
        model = Haystack
        fields = ['url', 'search_phrase', 'name']


class UploadFileForm(forms.Form):
    file = forms.FileField()

    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        self.error_class=BootstrapErrorList

    def clean_file(self):
        '''
        Check if uploaded file features correct syntax
        '''
        _file = self.cleaned_data["file"]
        for (num, line) in enumerate(_file):
            if len(line.split('|')) < 2:
                raise forms.ValidationError("Invalid file format in line %d: %s" % (num+1, line))
        return _file

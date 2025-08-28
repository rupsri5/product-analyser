from django import forms
from django.core.exceptions import ValidationError
from django.conf import settings
import os

from .models import ExcelFile


class ExcelFileForm(forms.ModelForm):
    """Form for uploading Excel files"""

    class Meta:
        model = ExcelFile
        fields = ['name', 'description', 'file', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a display name for this Excel file'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optional description of the file contents'
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control-file',
                'accept': '.xlsx,.xls'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

    def clean_file(self):
        """Validate uploaded file"""
        file = self.cleaned_data.get('file')

        if file:
            # Check file extension
            ext = os.path.splitext(file.name)[1].lower()
            if ext not in settings.ALLOWED_EXCEL_EXTENSIONS:
                raise ValidationError(
                    f'Invalid file type. Only {", ".join(settings.ALLOWED_EXCEL_EXTENSIONS)} files are allowed.'
                )

            # Check file size
            if file.size > settings.MAX_UPLOAD_SIZE:
                max_size_mb = settings.MAX_UPLOAD_SIZE / (1024 * 1024)
                raise ValidationError(
                    f'File size too large. Maximum allowed size is {max_size_mb} MB.'
                )

        return file

    def clean_name(self):
        """Validate name uniqueness"""
        name = self.cleaned_data.get('name')

        if name:
            # Check if name already exists (excluding current instance if editing)
            existing = ExcelFile.objects.filter(name=name)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)

            if existing.exists():
                raise ValidationError('An Excel file with this name already exists.')

        return name


class FilterForm(forms.Form):
    """Dynamic form for Excel data filtering"""

    def __init__(self, columns_data=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if columns_data:
            for column, values in columns_data.items():
                choices = [('', f'Select {column}...')] + [(val, val) for val in values]
                self.fields[column] = forms.ChoiceField(
                    choices=choices,
                    required=False,
                    widget=forms.Select(attrs={
                        'class': 'form-control filter-dropdown',
                        'data-column': column
                    })
                )

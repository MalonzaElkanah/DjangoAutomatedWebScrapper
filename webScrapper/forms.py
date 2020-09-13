from django import forms
from django.forms import ModelForm
from .models import Site, Scrapper


category=[
	('General', 'General'),
	('Bet Data', 'Bet Data'),
	('Online Jobs', 'Online Jobs'),
	('Jobs Appication', 'Jobs Appication'),
	('Images', 'Images'),
	('Pandemic', 'Pandemic'),
	('Test-File', 'Test File'),
]

class SiteModelForm(ModelForm):
	# name, status, date_created, description
	class Meta:
		model = Site
		fields = ('site_name', 'category', 'logo', 'description', 'ip_address')
		widgets = {
			'site_name': forms.TextInput(attrs={'class': 'form-control'}),
			'category': forms.Select(attrs={'class': 'form-control select'}, choices=category),
			'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
			'description': forms.Textarea(attrs={'class': 'form-control'}),
		}


class ScrapperModelForm(ModelForm):
	# name, status, date_created, description
	class Meta:
		model = Scrapper
		fields = ('site', 'url_scrapped', 'select_tag', 'data_type')

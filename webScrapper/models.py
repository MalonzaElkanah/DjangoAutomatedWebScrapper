from django.db import models
import csv

# Create your models here.


class Site(models.Model):
	site_name = models.CharField('Site', max_length=50)
	logo = models.ImageField('Logo', upload_to='Image/Data/Logo', default='dummy.png')
	ip_address = models.CharField('IP ip_address', max_length=20, blank=True, null=True)
	category = models.CharField('Select Tag', max_length=100)	
	description = models.CharField('Description', max_length=200, blank=True)
	date_created = models.DateTimeField('Date Created', auto_now_add=True)
	# site_name, logo, category, description, ip_address	

	def __str__(self):
		return self.site_name	

	def my_scrappers(self):
		return Scrapper.objects.filter(site=self.id)


class Scrapper(models.Model):
	site = models.ForeignKey(Site, on_delete=models.CASCADE)
	url_scrapped = models.CharField('url', max_length=1000)
	select_tag = models.CharField('Select Tag', max_length=100)
	data_type = models.CharField('Data Type', max_length=10, default='TEXT')
	# site, url_scrapped, select_tag

	def my_runs(self):
		return ScrapperRun.objects.filter(scrapper=self.id)


class ScrapperRun(models.Model):
	scrapper = models.ForeignKey(Scrapper, on_delete=models.CASCADE)
	date_scrapped = models.DateTimeField('Date Created', auto_now_add=True)
	data_scrapped = models.FileField('Data File', upload_to='File/Data/ScrappedFiles', max_length=100000)
	status = models.CharField('Status', max_length=10)
	category = models.CharField('Category', max_length=20, default='not_view')
	# scrapper, date_scrapped, data_scrapped, status

	def csv_data(self):
		csv_file = self.data_scrapped
		f = open(csv_file.path)
		reader = csv.reader(f)
		reader = enumerate(csv.reader(f))
		return reader

	def csv_column_count(self):
		csv_file = self.data_scrapped
		f = open(csv_file.path)
		reader = csv.reader(f)
		reader = enumerate(csv.reader(f))
		for i, row in reader:
			if i == 0:
				count = []
				j = 0
				for data in row:
					count = count + [j]
					j = j + 1
				return count

	def data_url(self):
		url_name = self.data_scrapped.name
		url_list = url_name.split('/')
		index = url_list.index('Uploads')
		m = url_list[index:-1] + [url_list[-1]]
		url = '/'.join(m)
		return '../' + url

	def data_name(self):
		url_name = self.data_scrapped.name
		url_list = url_name.split('/')
		return url_list[-1]


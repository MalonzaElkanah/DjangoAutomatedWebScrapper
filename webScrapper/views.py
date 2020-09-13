from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, StreamingHttpResponse
from django.conf import settings
from django.core.files import File

from .forms import SiteModelForm, ScrapperModelForm
from .models import Site, Scrapper, ScrapperRun

import requests, bs4, csv, subprocess, threading
import datetime as dt

# Create your views here.


def index(request):
	sites = Site.objects.all()
	scrappers = Scrapper.objects.all()
	runs = ScrapperRun.objects.all()
	forms= {}
	for site in sites:
		form = SiteModelForm(instance=site)
		forms.setdefault(site, form)
	return render(request, 'data/index.html', {"sites": sites, "scrappers": scrappers, 
		"forms": forms, "runs": runs})


def create_site(request):
	if request.is_ajax():
		new_data = {
			'site_name': request.POST['site_name'], 'category': request.POST['category'], 
			'description': request.POST['description']
		}
		form = SiteModelForm(request.POST, request.FILES)
		if form.is_valid():
			data = form.save()
			form_num = int(request.POST['form_num'])
			form_num = form_num + 1
			for x in range(1,form_num):
				url = 'url_scrapped_'+str(x)
				select = 'select_tag_'+str(x)
				data_type = 'data_type_'+str(x)
				try:
					url = request.POST[''+url+'']
					select = request.POST[''+select+'']
					data_type = request.POST[''+data_type+'']
					scrapper_data = {
						'site':data.id, 'url_scrapped': url, 'select_tag': select, 'data_type': data_type
					}
					form1 = ScrapperModelForm(scrapper_data)
					if form1.is_valid():
						form1.save()
					else:
						return JsonResponse({"error": form1.errors}, status=200)
				except Exception:
					name_list = ''
			return JsonResponse({"success": "Site Created"}, status=200)
		else:
			return JsonResponse({"error": form.errors}, status=200)
	else:
		return HttpResponseRedirect('../../web/')


def update_site(request):
	if request.is_ajax():
		# Update Site
		id = int(request.POST['id'])
		site = Site.objects.get(id=id)
		form = SiteModelForm(request.POST, request.FILES, instance=site)
		if form.is_valid():
			form.save()
		else:
			return JsonResponse({"error": form.errors}, status=200)
		# Update OLd Scrapper
		scrappers = Scrapper.objects.filter(site=id)
		for scrapper in scrappers:
			url = request.POST['url_scrapped'+str(scrapper.id)+'']
			tag = request.POST['select_tag'+str(scrapper.id)+'']
			scrapper_id = request.POST['id'+str(scrapper.id)+'']
			data_type = request.POST['data_type'+str(scrapper.id)+'']
			try:
				data = {
					'site': site.id, 'url_scrapped': url, 'select_tag': tag, 'data_type': data_type
				}
				form1 = ScrapperModelForm(data, instance=scrapper)
				if form1.is_valid():
					form1.save()
				else:
					return JsonResponse({"error": form1.errors}, status=200)
			except Exception:
				name= ''
				time_estimate = ''
				status = ''
		# Add New Milestones
		form_num = int(request.POST['form_numEdit'])
		form_num = form_num + 1
		for x in range(1,form_num):
			url = 'url_scrapped_'+str(x)
			select = 'select_tag_'+str(x)
			data_type = 'data_type_'+str(x)
			try:
				url = request.POST[''+url+'']
				select = request.POST[''+select+'']
				data_type = request.POST[''+data_type+'']
				scrapper_data = {
					'site':site.id, 'url_scrapped': url, 'select_tag': select, 'data_type': data_type
				}
				form2 = ScrapperModelForm(scrapper_data)
				if form2.is_valid():
					form2.save()
				else:
					return JsonResponse({"error": form2.errors}, status=200)
			except Exception:
				url = ''
		return JsonResponse({"success": "Site Updated"}, status=200)
	else:
		return HttpResponseRedirect('../../web/')


def delete_site(request, site_id):
	if request.is_ajax():
		id = int(site_id)
		get_id = int(request.GET['delete_id'])
		if get_id == id:
			delete_data = Site.objects.get(id=get_id).delete()
			return JsonResponse({"success": "Site Deleted"}, status=200)
		else:
			return JsonResponse({"error": "Unexpected Error Occurred"}, status=200)
	else:
		return HttpResponseRedirect('../../web/') 


def scrap_site(request):
	if request.is_ajax():
		id = int(request.GET['scrapper_id'])
		scrapper = Scrapper.objects.get(id=id)
		threadObj = threading.Thread(target=data_scrapping, args=[scrapper])
		threadObj.start()
		return JsonResponse({"success": "Scrapping Data Started"}, status=200)
	else:
		return HttpResponseRedirect('../../web/') 


def delete_scrapper(request, scrapper_id):
	if request.is_ajax():
		id = int(scrapper_id)
		get_id = int(request.GET['delete_id']);
		if get_id == id:
			delete_data = Scrapper.objects.get(id=get_id).delete()
			return JsonResponse({"success": "Scrapper Deleted"}, status=200)
		else:
			return JsonResponse({"error": "Unexpected Error Occurred"}, status=200)
	else:
		return HttpResponseRedirect('../../web/') 

# NON VIEWS Functions
def data_scrapping(scrapper):
	url = scrapper.url_scrapped
	tag = scrapper.select_tag
	today = dt.datetime.now()
	t = str(f"{today:%Y%m%d%H%M%S}")
	if scrapper.site.category == 'Test-File':
		file = open(url)
		soup = bs4.BeautifulSoup(file)
		elnts = soup.select(tag)
		path = settings.LOCAL_FILE_DIR + '/Uploads/File/Data/ScrappedFiles/scrapper'+t+'.csv'
		# data_file = open(path, 'a')
		outputFile = open(path, 'w', newline='')
		outputWriter = csv.writer(outputFile)
		for elnt in elnts:
			raw_data = elnt.getText()
			lists = raw_data.split('\n')
			new_list = []
			# data_file.write('[')
			for l in lists:
				if not l == "":
					new_list = new_list + [l]
					
					# data_file.write(str(l)+', ')
			# data_file.write(']\n')
			outputWriter.writerow(new_list)
		# scrapper, date_scrapped, data_scrapped, status
		outputFile.close()
		# data_file.close()
		with open(path) as f:
			file = File(f)
			data = ScrapperRun(scrapper=scrapper, date_scrapped=str(f"{today:%Y-%m-%d %H:%M:%S}"), 
				data_scrapped=file, status='Completed', category='not_view')
			data.save()
		return data
	else:
		res = requests.get(url)
		res.raise_for_status()
		soup = bs4.BeautifulSoup(res.text)
		elnts = soup.select(tag)
		path = settings.LOCAL_FILE_DIR + '/Uploads/File/Data/ScrappedFiles/scrapper'+t+'.csv'
		outputFile = open(path, 'w', newline='')
		outputWriter = csv.writer(outputFile)
		for elnt in elnts:
			raw_data = elnt.getText()
			lists = raw_data.split('\n')
			new_list = []
			for l in lists:
				if not l == "":
					new_list = new_list + [l]
			outputWriter.writerow(new_list)
		outputFile.close()
		with open(path) as f:
			file = File(f)
			data = ScrapperRun(scrapper=scrapper, date_scrapped=str(f"{today:%Y-%m-%d %H:%M:%S}"), 
				data_scrapped=file, status='Completed')
			data.save()
		return data
					
def delete_run(request, run_id):
	if request.is_ajax():
		id = int(run_id)
		get_id = int(request.GET['delete_id']);
		if get_id == id:
			delete_data = ScrapperRun.objects.get(id=get_id)
			delete_data.data_scrapped.delete()
			delete_data.delete()
			return JsonResponse({"success": "Data Deleted"}, status=200)
		else:
			return JsonResponse({"error": "Unexpected Error Occurred"}, status=200)
	else:
		return HttpResponseRedirect('../../web/')


def check_run(request, run_id):
	if request.is_ajax():
		id = int(run_id)
		get_id = int(request.GET['update_id']);
		if get_id == id:
			delete_data = ScrapperRun.objects.filter(id=get_id).update(category='viewed')
			return JsonResponse({"success": "Data Checked"}, status=200)
		else:
			return JsonResponse({"error": "Unexpected Error Occurred"}, status=200)
	else:
		return HttpResponseRedirect('../../web/')

from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Messages ,UserInformations ,ConfirmToken
from .forms import LoginForm ,RegisterForm ,Upload ,Confirm ,Search
from .tools import ConfirmTool
from django.db.models import Q
from django.http import HttpResponse ,HttpResponseRedirect
from django.shortcuts import get_list_or_404, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.postgres.search import TrigramSimilarity 
def chat(request,uid="23"):
	return render(request,"chat.html",{})

# def conversations(request):
# 	return render(request,"conversations.html",{})

# def do(request):
# 	return render(request,"2.html",{})

def index(request):
    return render(request, 'index.html', {})

def room(request, room_name):
    return render(request, 'room.html', {
        'room_name': room_name
    })

def login_required_api(function):
	def wrapper(request, *args, **kw):
		if not request.user.is_authenticated:
			return HttpResponseRedirect("/bot/login")
		user = user.username 
		return function(request, user)
	return wrapper

@login_required_api
def sync_messages(request,user):
	data = json.loads(str(request.body,'utf-8'))
	target ,index ,messages = User.objects.get(username=data['target']) ,data['index'] ,[]
	objects = Messages.objects.filter(Q(target=target,sender=user) | Q(target=sender,sender=target)).order_by('-timestamp').count(50)
	messages = [ [{"text":obj.text,"time":obj.create},"out" if obj.sender == sender else "in"] for obj in objects ]
	return HttpResponse(json.dumps(messages),content_type="application/json")



def login(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect("/chat")
	if request.method == 'POST':
		login_form = LoginForm(request.POST or None)
		register_form = RegisterForm(request.POST or None)
		
		if login_form.is_valid():
			username = login_form.cleaned_data['username']
			password = login_form.cleaned_data['password']
			user = authenticate(request, username=username, password=password)
		
			if user is not None:
				login(request,user)
				return HttpResponseRedirect("/chat")
			else:
				return render(request, 'login.html', {'login': LoginForm(),"register":RegisterForm(),"incorrect":True})
		
		elif register_form.is_valid:
			
			name = register_form.cleaned_data['name']
			lastname = register_form.cleaned_data.get('lastname',None)
			username = register_form.cleaned_data['username']
			email = register_form.cleaned_data['email']
			
			user_informations = UserInformations()
			user_informations.firstname = name
			user_informations.lastname = lastname
			user_informations.username = username
			user_informations.email = email
			user_informations.save()
			
			confirm_token = ConfirmToken()
			confirm_token.token = ConfirmTool.generateConfirmToken()
			confirm_token.user = user_informations
			confirm_token.save()

			return HttpResponseRedirect("/confirm/%s"%token)

	return render(request, 'login.html', {'login': LoginForm() ,"register":RegisterForm()})

def profile(request):
	return render(request,"profile.html",{})

def landing(request):
	return render(request,"landing.html",{"search":Search()})

def new(request):
	print("start...")
	if request.method == 'POST':
		form = Upload(request.POST, request.FILES)
		print(form.errors)
		print(request.FILES.keys())
		if form.is_valid():
			
			path = 'media/s'
			f = request.FILES['file']
			destination = open(path, 'wb+')
			for chunk in f.chunks():
				print(1)
				destination.write(chunk)
			destination.close()

	return render(request,'new.html',{'upload':Upload()})

def upload(request):
	print("start...")
	if request.method == 'POST':
		form = Upload(request.POST, request.FILES)
		print(form.errors)
		print(request.FILES.keys())
		if form.is_valid():
			
			path = 'media/s'
			f = request.FILES['file']
			destination = open(path, 'wb+')
			for chunk in f.chunks():
				print(1)
				destination.write(chunk)
			destination.close()

	return render(request,'upload.html',{'upload':Upload()})

def confirm(request,token):
	confirm_token = get_object_or_404(ConfirmToken,token=token)
	if request.method == 'POST':
		form = Upload(request.POST, request.FILES)

		if form.is_valid():
			password = register_form.cleaned_data['password']
			bio = register_form.cleaned_data['bio']
			path = 'media/%s'%ConfirmTool.generateConfirmToken()
			f = request.FILES['file']
			destination = open(path, 'wb+')
			for chunk in f.chunks():
				destination.write(chunk)
			destination.close()
			user_informations = confirm_token.user
			user_informations.bio = bio
			user_informations.owner = User.objects.create_user(user.username, user.email, password)
			user_informations.profile_picture = "/%s"%path
			user_informations.save()
	return render(request,"confirm.html",{'confirm':Confirm()})

@csrf_exempt
def auto_complete(request):
	data = json.loads(str(request.body,'utf-8'))
	objects = User.objects.filter(username__startswith=data['username'])
	results = [obj.username for obj in objects[:5]]
	return HttpResponse(json.dumps(results),content_type="application/json")

from django.core.cache import cache
def get_upload_progress(request):
  cache_key = "%s_%s" % (request.META['REMOTE_ADDR'], request.GET['X-Progress-ID'])
  data = cache.get(cache_key)
  return HttpResponse(json.dumps(data))
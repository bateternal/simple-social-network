from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Messages ,UserInformations ,ConfirmToken ,Posts ,Conversations
from .forms import LoginForm ,RegisterForm ,Upload ,Confirm ,Search, Test
from .tools import ConfirmTool
from django.db.models import Q
from django.http import HttpResponse ,HttpResponseRedirect
from django.shortcuts import get_list_or_404, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json
import os
from django.contrib.auth import authenticate, login
from django.contrib.postgres.search import TrigramSimilarity 
from time import time
from django.contrib.auth import logout
from random import randint
import base64

MEDIA_DIRECTORY = os.environ.get('MEDIA_DIRECTORY')

@csrf_exempt
def confirm(request, token):
	if request.user.is_authenticated:
		return HttpResponseRedirect("/landing")
	try:
		confirm_token = get_object_or_404(ConfirmToken,token=token)
		if request.method == 'POST':
			data = json.loads(str(request.body,'utf-8'))
			password = data['password']
			bio = data['bio']

			path = '/%s/%s.jpg'%(os.environ.get('MEDIA_DIRECTORY'), ConfirmTool.generateConfirmToken())
			file = data['file']
			
			imgdata = base64.b64decode(file[23:])
			
			with open(path, 'wb') as f:
				f.write(imgdata)
			user_informations = confirm_token.user
			user_informations.bio = bio
			user_informations.owner = User.objects.create_user(user_informations.username, user_informations.email, password)
			user_informations.profile_picture = path
			user_informations.save()
			login(request,user_informations.owner)
			return HttpResponse(json.dumps({"ok":True}))
		return render(request,"confirm.html",{'confirm':Confirm()})
	except:
		return notfound(request)

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/login')

def other(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect("/login")
	return HttpResponseRedirect('/landing')

def notfound(request):
	return HttpResponse("<html><style>body {background-image: url('/media/AsahNlC0VhQ');background-position: center;background-repeat: no-repeat;background-size: cover;margin: 0; height: 100%; }</style><body></body></html>")

def chat(request, username):
	if not request.user.is_authenticated:
		return HttpResponseRedirect("/login")
	try:
		informations = UserInformations.objects.get(owner=User.objects.get(username=username))
		return render(request,"chat.html",{"room_name":username,"me":request.user.username,
						"name":informations.firstname,"pic":informations.profile_picture })
	except:
		return notfound(request)

def home(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect("/login")
	try:
		user = UserInformations.objects.get(owner=request.user)
		return render(request,"home.html",{"pic":user.profile_picture,"firstname":user.firstname,
									"lastname":user.lastname,"bio":user.bio})
	except:
		return notfound(request)

@csrf_exempt
def allconversations(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect("/login")
	try:
		objects = Conversations.objects.filter(user=request.user).order_by('-create')
		data = []
		for obj in objects:
			user = UserInformations.objects.get(owner=obj.target)
			data.append({"username":user.username,"pic":user.profile_picture,"date":obj.date,"text":obj.text,"seeing":obj.seeing})

		return HttpResponse(json.dumps(data),content_type='application/json')
	except:
		return notfound(request)

@csrf_exempt
def sync_messages(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect("/login")
	try:
		data = json.loads(str(request.body,'utf-8'))
		target ,index ,messages,user = User.objects.get(username=data['target']) ,data.get('index',0) ,[] ,User.objects.get(username=data['sender'])
		sender_id = user.id
		target_id = target.id
		query = 'select * from chat_messages where ("target_id"=%i and "sender_id"=%i) or ("sender_id"=%i and "target_id"=%i) order by id desc limit 10;'%(sender_id,target_id,sender_id,target_id)
		objects = Messages.objects.raw(query)

		messages = [[{"text":obj.text,"date":obj.date,"pk":obj.id},"out" if obj.sender == user else "in"] for obj in objects ]
		Conversations.objects.filter(user=request.user,target=target).update(seeing=True)

		return HttpResponse(json.dumps(messages[::-1]),content_type="application/json")
	except:
		return notfound(request)

@csrf_exempt
def see_message(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect("/login")
	try:
		data = json.loads(str(request.body,'utf-8'))
		Conversations.objects.filter(user=request.user,target=User.objects.get(data['target'])).update(seeing=True)
		return HttpResponse(json.dumps({'errorcode':0,'success':True}))
	except:
		return notfound(request)

@csrf_exempt
def add_message(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect("/login")
	try:	
		data = json.loads(str(request.body,'utf-8'))
		if request.user.username == data['sender']:
			message = Messages()
			message.sender = User.objects.get(username=data['sender'])
			message.target = User.objects.get(username=data['target'])
			message.timestamp = time()
			message.text = data['text']
			message.date = data['date']
			message.save()
			return HttpResponse(json.dumps({'errorcode':0,'success':True}))
	except:
		return notfound(request)

def login_user(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect("/landing")
	try:
		if request.method == 'POST':
			login_form = LoginForm(request.POST or None)
			register_form = RegisterForm(request.POST or None)
			
			if login_form.is_valid():
				username = login_form.cleaned_data['lusername']
				password = login_form.cleaned_data['lpassword']
				user = authenticate(request, username=username, password=password)
			
				if user is not None:
					login(request,user)
					return HttpResponseRedirect("/landing")
				else:
					return render(request, 'login.html', {'login': LoginForm(),"register":RegisterForm(),"incorrect":True})
			
			elif register_form.is_valid():
				
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

				return HttpResponseRedirect("/confirm/%s"%confirm_token.token)

		return render(request, 'login.html', {'login': LoginForm() ,"register":RegisterForm()})
	except:
		return notfound(request)

def profile(request, username):
	if not request.user.is_authenticated:
		return HttpResponseRedirect("/login")
	try:
		if request.user.username == username:
			return home(request)
		informations = UserInformations.objects.get(owner=User.objects.get(username=username))
		return render(request,"profile.html",{"username":username,"firstname":informations.firstname,
											"lastname":informations.lastname,"bio":informations.bio,
											"pic":informations.profile_picture })
	except:
		return notfound(request)

def landing(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect("/login")
	return render(request,"landing.html",{"search":Search(),"user":request.user.username})

def new(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect("/login")
	try:
		if request.method == 'POST':
			form = Upload(request.POST, request.FILES)

			if form.is_valid():
				
				title = form.cleaned_data['title']
				content = form.cleaned_data.get('content',None)
				path = 'media/%s'%ConfirmTool.generateConfirmToken()

				file = request.FILES.get('file',None)
				if file is not None:
					destination = open(path, 'wb+')
					for chunk in file.chunks():
						destination.write(chunk)
					destination.close()
					path = "/" + path
				else:
					path = None
				post = Posts()
				post.content = content
				post.title = title
				post.file = path
				post.owner = request.user
				post.save()
				return HttpResponseRedirect("/home")
		user = UserInformations.objects.get(owner=request.user)		
		return render(request,'new.html',{'upload':Upload(),"pic":user.profile_picture,"confirm":Confirm()})
	except:
		return notfound(request)

def conversations(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect("/login")	
	return render(request,'conversations.html',{})

@csrf_exempt
def get_posts(request,username=None):
	if not request.user.is_authenticated:
		return HttpResponseRedirect("")
	try:
		data = []
		posts = Posts.objects.filter(owner=(username and User.objects.get(username=username) or request.user))
		for post in posts:
			payload = {}
			if post.file:
				payload["is_file"] = True
				payload["file"] = post.file
			payload["title"] = post.title
			payload["content"] = post.content or ""
			payload["pk"] = post.pk
			data.append(payload)
		return HttpResponse(json.dumps(data),content_type='application/json')
	except:
		return notfound(request)	

@csrf_exempt
def delete_post(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect("/login")
	data  = json.loads(str(request.body,'utf-8'))
	try:
		Posts.objects.get(owner=request.user,pk=data["pk"]).delete()
		return HttpResponse(json.dumps({'errorcode':0,'success':True}))
	except:
		return notfound(request)

@csrf_exempt
def auto_complete(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect("/login")
	try:
		data = json.loads(str(request.body,'utf-8'))
		objects = User.objects.filter(username__startswith=data['username'])
		results = [obj.username for obj in objects[:5]]
	except:
		return notfound(request)
	return HttpResponse(json.dumps(results),content_type="application/json")

# from django.core.cache import cache
# def get_upload_progress(request):
#   cache_key = "%s_%s" % (request.META['REMOTE_ADDR'], request.GET['X-Progress-ID'])
#   data = cache.get(cache_key)
#   return HttpResponse(json.dumps(data))


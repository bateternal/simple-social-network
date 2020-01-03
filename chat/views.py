from django.shortcuts import render

def chat(request):
	return render(request,"chat.html",{})

def conversations(request):
	return render(request,"conversations.html",{})

def do(request):
	return render(request,"2.html",{})

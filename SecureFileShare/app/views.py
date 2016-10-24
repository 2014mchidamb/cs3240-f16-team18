from django.shortcuts import render, render_to_response, HttpResponse

# Create your views here.

def index(request):
	return render_to_response('index.html')

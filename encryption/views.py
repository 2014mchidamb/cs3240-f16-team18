from django.shortcuts import render
from .forms import PublicKeyForm, FileKeyForm
from .models import PublicKey, FileKey
from reports.models import Viewership

# Create your views here.
def add_publickey(request):
	if request.method == 'POST':
		form = PublicKeyForm(request.POST)
		if form.is_valid():
			model = form.save()
			model.save()

def get_publickey(request):
    if request.method == 'GET':
        return render(request, template_name='encryption/public_key.html', context={"public_key": PublicKey.objects.get(user=request.user.username)})


def add_filekey(request):
    if request.method == 'POST':
        form = FileKeyForm(request.POST)
        if form.is_valid():
            model = form.save()
            model.save()


def get_filekey(request):
    if request.method == 'POST':
        return render(request, template_name='encryption/file_key.html', context={"file_key": PublicKey.objects.get(public_key=request.POST['public_key'], file=request.POST['file'])})

def get_target_keys(request):
    if request.method == "POST":
        target_keys = Viewership.objects.filter(user=request.user.username) # TODO: Fix this
        return render(request, template_name='encryption/target_keys.html', context={"target_keys": target_keys})
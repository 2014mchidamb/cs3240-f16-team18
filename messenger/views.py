from Crypto.PublicKey import RSA
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from messenger.forms import SendForm
from .models import Message


# Create your views here.

@login_required
def send(request):
	if not request.user.profile.active:
		return render(request, template_name='suspended.html')
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = SendForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
			# ...
			# redirect to a new URL:
			model = form.save(commit=False)
			model.sender = request.user.username
			if model.encrypted:
				recipient = User.objects.get(username=model.recipient)
				pub_key_obj = RSA.importKey(recipient.profile.pub_key)
				print model.text
				emsg = pub_key_obj.encrypt(str.encode(str(model.text)), 'x')[0]
				model.text = emsg
			model.save()
			messages.success(request, 'Your message was sent!')
		else:
			messages.error(request, 'Please correct the error below.')

	# if a GET (or any other method) we'll create a blank form
	else:
		form = SendForm()

	return render(request, template_name='messenger/send.html', context={'form': form})

@login_required
def read(request):
	if not request.user.profile.active:
		return render(request, template_name='suspended.html')
	return render(request, template_name='messenger/read_messages.html', context={
		'read_messages': Message.objects.filter(recipient__iexact=request.user.username, read=True),
		'unread_messages': Message.objects.filter(recipient__iexact=request.user.username, read=False)
	})

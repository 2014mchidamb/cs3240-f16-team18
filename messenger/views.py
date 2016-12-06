from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
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
			recipient = User.objects.get(username=model.recipient)
			if model.encrypted:
				pub_key_obj = RSA.importKey(recipient.profile.pub_key)
				model.etext = pub_key_obj.encrypt(model.text.encode('latin-1'), 'x')[0]
			model.save()
			recipient.profile.unread += 1
			recipient.save()
			return redirect('/messenger/read/')
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
	for key in request.POST:
		if 'decrypt' in key:
			msg = Message.objects.get(id=int(key[7:]))
			msg.encrypted = False
			msg.save()
			return redirect('/messenger/read/')
		if 'unread' in key:
			msg = Message.objects.get(id=int(key[6:]))
			msg.read = False
			msg.save()
			user = User.objects.get(username=request.user.username)
			user.profile.unread += 1
			user.save()
			return redirect('/messenger/read/')
		if 'read' in key:
			msg = Message.objects.get(id=int(key[4:]))
			msg.read = True
			msg.save()
			user = User.objects.get(username=request.user.username)
			user.profile.unread -= 1
			user.save()
			return redirect('/messenger/read/')
	return render(request, template_name='messenger/read_messages.html', context={
		'read_messages': Message.objects.filter(recipient__iexact=request.user.username, read=True),
		'unread_messages': Message.objects.filter(recipient__iexact=request.user.username, read=False)
	})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from messenger.forms import SendForm
from .models import Message


# Create your views here.

@login_required
def send(request):
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
    return render(request, template_name='messenger/read_messages.html', context={"messages": Message.objects.filter(recipient__iexact=request.user.username)})

@login_required
def send_message(request):
    #if(request.POST["encrypt_status"]):
        #msg = Message(text=request.POST["text"], sender = request.user.username, recipient = request.POST["recipient"], encryptedFlag= True)
        # do encryption here.
        #codedMsg = enc(msg)
        #codedMsg.save()
    #else:
        msg = Message(text=request.POST["text"], sender=request.user.username, recipient=request.POST["recipient"], encryptedFlag=False)
        msg.save()

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Message


# Create your views here.

@login_required
def send(request):
    return render(request, template_name='messenger/send.html')

@login_required
def read(request):
    return render(request, template_name='messenger/read_messages.html', context={"messages": Message.objects.filter(recipient__iexact=request.user.username)})

@login_required
def send_message(request):
    if(request.POST["encrypt_status"]):
        #do encryption here.
        msg = Message(text=request.POST["text"], sender = request.user.username, recipient = request.POST["recipient"], encryptedFlag= True)
        msg.save()
    else:
        msg = Message(text=request.POST["text"], sender=request.user.username, recipient=request.POST["recipient"], encryptedFlag=False)
        msg.save()
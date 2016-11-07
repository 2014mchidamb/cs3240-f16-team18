from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, render_to_response, HttpResponse
from django.template import RequestContext
from .models import Message
# Create your views here.

@login_required
def send(request):
    return render(request, template_name='messenger/send.html')

@login_required
def read(request):
    return render(request, template_name='messenger/read_messages.html')

@login_required
def send_message(request):
    msg = Message(text=request.POST["I can do text."], sender = request.POST["sender"], recipient = request.POST["recipient"], encryptedFlag= False)
    msg.save()
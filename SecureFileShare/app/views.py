from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, render_to_response, HttpResponse
from django.template import RequestContext
from .forms import ProfileForm, UserForm
from .models import Profile

# Create your views here.

def index(request):
	return render(request, template_name='index.html')

@login_required
def profile(request):
	return render(request, template_name='registration/profile.html')

@login_required
def update_profile(request):
	if request.method == 'POST':
		user_form = UserForm(request.POST, instance=request.user)
		profile_form = ProfileForm(request.POST, instance=request.user.profile)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			messages.success(request, 'Your profile was successfully updated!')
			return redirect('/accounts/profile/')
		else:
			messages.error(request, 'Please correct the error below.')
	else:
		user_form = UserForm(instance=request.user)
		profile_form = ProfileForm(instance=request.user.profile)
	return render(request, 'registration/edit_profile.html', {
			'user_form': user_form,
			'profile_form': profile_form
	})

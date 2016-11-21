from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, render_to_response, HttpResponse
from django.template import RequestContext
from .forms import ProfileForm, UserForm, GroupForm
from .models import Group, Membership, Profile

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
			messages.success(request, 'Your profile was updated!')
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

@login_required
def groups(request):
	mygroups = Group.objects.filter(members__username__exact=request.user.username)
	return render(request, 'registration/groups.html', {
			'mygroups': mygroups
	})

@login_required
def create_groups(request):
	if request.method == 'POST':
		group_form = GroupForm(request.POST)
		if group_form.is_valid():
			group_form.save()
			g = Group.objects.get(name=group_form.cleaned_data['name'])
			m = Membership(user=request.user, group=g)
			m.save()
			messages.success(request, 'You successfull created a group!')
			return redirect('/accounts/groups/')
		else:
			messages.error(request, 'Please correct the error below.')
	else:
		group_form = GroupForm()
	return render(request, 'registration/create_groups.html', {
		'group_form': group_form
	})

@login_required
def view_group(request, group_name):
	group = Group.objects.get(name=group_name)
	return render(request, 'registration/group_profile.html', {
		'group': group,
		'members': group.members.all()
	})

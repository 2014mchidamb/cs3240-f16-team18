from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, render_to_response, HttpResponse
from django.template import RequestContext
from .forms import ProfileForm, UserForm, GroupForm, AddUserForm, DelUserForm
from .models import Group, Membership, Profile

# Create your views here.

def index(request):
	return render(request, template_name='index.html')

@login_required
def profile(request):
	if not request.user.profile.active:
		return render(request, template_name='suspended.html')
	return render(request, template_name='registration/profile.html')

@login_required
def view_profile(request, username):
	if not request.user.profile.active:
		return render(request, template_name='suspended.html')
	user = User.objects.get(username=username)
	if 'suspend' in request.POST:
		user.profile.active = False
		user.save()
		return redirect('/public/users/')
	if 'activate' in request.POST:
		user.profile.active = True
		user.save()
		return redirect('/public/users/')
	if 'makesm' in request.POST:
		user.profile.site_manager = True
		user.save()
		return redirect('/public/users/')
	return render(request, 'registration/view_profile.html', {
		'user': user,
		'is_sm': request.user.profile.site_manager
	})

@login_required
def update_profile(request):
	if not request.user.profile.active:
		return render(request, template_name='suspended.html')
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
	if not request.user.profile.active:
		return render(request, template_name='suspended.html')
	mygroups = Group.objects.filter(members__username__exact=request.user.username)
	if request.user.profile.site_manager:
		mygroups = Group.objects.all()
	return render(request, 'registration/groups.html', {
			'mygroups': mygroups
	})

@login_required
def create_groups(request):
	if not request.user.profile.active:
		return render(request, template_name='suspended.html')
	if request.method == 'POST':
		group_form = GroupForm(request.POST)
		if group_form.is_valid():
			group_form.save()
			g = Group.objects.get(name=group_form.cleaned_data['name'])
			m = Membership(user=request.user, group=g)
			m.save()
			messages.success(request, 'You successfully created a group!')
			return redirect('/accounts/groups/')
		else:
			messages.error(request, 'Please correct the error below.')
	else:
		group_form = GroupForm()
	return render(request, 'registration/create_groups.html', {
		'group_form': group_form
	})

@login_required
def edit_group(request, group_name):
	if not request.user.profile.active:
		return render(request, template_name='suspended.html')
	group = Group.objects.get(name=group_name)
	is_member = group.members.filter(username=request.user.username)
	if request.user.profile.site_manager:
		is_member = True
	if request.method == 'POST':
		group_form = GroupForm(request.POST, instance=group)
		if group_form.is_valid():
			group_form.save()
			return redirect('/accounts/groups/')
		else:
			messages.error(request, 'Please correct the error below.')
	else:
		group_form = GroupForm(instance=group)
	return render(request, 'registration/edit_groups.html', {
		'group_form': group_form,
		'cant_edit': not is_member
	})		

@login_required
def view_group(request, group_name):
	if not request.user.profile.active:
		return render(request, template_name='suspended.html')
	group = Group.objects.get(name=group_name)
	is_member = group.members.filter(username=request.user.username)
	cant_view = group.priv and not is_member
	if request.user.profile.site_manager:
		is_member = True
		cant_view = False
	if 'leave' in request.POST:
		print("Made it here")
		m = Membership.objects.get(user=request.user, group=group)
		m.delete()
		return redirect('/public/groups')
	elif 'join' in request.POST:
		m = Membership(user=request.user, group=group)
		m.save()
		return redirect('/public/groups')
	if 'add_user' in request.POST:
		add_form = AddUserForm(request.POST)
		if add_form.is_valid():
			user_to_add = User.objects.filter(username=add_form.cleaned_data['username']).first()
			if user_to_add:
				m = Membership(user=user_to_add, group=group)
				m.save()
			return redirect('/groups/'+group_name)
	else:
		add_form = AddUserForm()
	if 'del_user' in request.POST:
		del_form = DelUserForm(request.POST)
		if del_form.is_valid():
			user_to_del = User.objects.filter(username=del_form.cleaned_data['user_to_del']).first()
			if user_to_del:
				m = Membership.objects.get(user=user_to_del, group=group)
				m.delete()
			return redirect('/groups/'+group_name)
	else:
		del_form = DelUserForm()
			
	return render(request, 'registration/group_profile.html', {
		'group': group,
		'members': group.members.all(),
		'is_member': is_member,
		'cant_view': cant_view,
		'add_form': add_form,
		'del_form': del_form
	})

@login_required
def public_groups(request):
	if not request.user.profile.active:
		return render(request, template_name='suspended.html')
	pubgroups = Group.objects.filter(priv=False)
	return render(request, 'registration/public_groups.html', {
		'pubgroups': pubgroups
	})

@login_required
def public_users(request):
	if not request.user.profile.active:
		return render(request, template_name='suspended.html')
	pubusers = User.objects.filter(profile__priv=False)
	return render(request, 'registration/public_users.html', {
		'pubusers': pubusers
	})

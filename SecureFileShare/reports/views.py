from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import ReportsTree
from .models import Files
import json

from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
	return render(request, template_name='index.html')

@login_required
def view_my_reports(request):
	treeCont = ReportsTree.objects.filter(owner__iexact=request.user.username)
	
	#treeCont.delete()
	if len(treeCont) == 0:
		newTree = ReportsTree(owner = request.user.username, treeStruct = json.dumps(["topFolder", ["directory", "File:MyNameIsJohn.txt", ["newFolder"]]]))
		print(newTree.treeStruct)
		newTree.save()
	
	preEncVal = treeCont[0].treeStruct
	encodedVal = json.loads(preEncVal)
	
	print(encodedVal)
	
	return render(request, template_name='reports/directory.html', context={"dirStruct": displayTree(encodedVal)})

	
def file_get(request):
	requested = request.GET
	gotten = requested.get('name')
	
	usersFiles = Files.objects.filter(owner__iexact=request.user.username)
	
	print("uname", request.user.username)
	
	nameMatch = None
	for item in usersFiles:
		if item.name == gotten:
			nameMatch = item
			break
	
	if nameMatch is None:
		return render(request, template_name='reports/filemake.html', context={"fileData": ""})
	
	content_load = nameMatch.fileCont
	
	return render(request, template_name='reports/filemake.html', context={"fileData": content_load})

def file_list(request):
	usersFiles = Files.objects.filter(owner__iexact=request.user.username)
	print(usersFiles)
	
	if len(usersFiles) == 0:
		newFile = Files(owner = request.user.username, name = "ReadMe.txt", fileCont = "Welcome to SecureFileShare.  Try uploading more files here.")
		newFile.save()
		return file_list(request)
	
	list_names = []
	for files in usersFiles:
		list_names.append(files.name)
		
	dispVal = (str(list_names)).replace("'","")
	
	return render(request, template_name='reports/filemake.html', context={"fileData": dispVal})

@csrf_exempt 
def file_upload(request):
	requested = request.POST
	gotten = requested['name']
	cont   = requested['cont']
	print(gotten,cont)
	newFile = Files(owner = request.user.username, name = gotten, fileCont = cont)
	newFile.save()
	
	return render(request, template_name='reports/filemake.html', context={"fileData": "success"})

def displayTree(dir):
	return dispTreeHelp(dir, 0);

def dispTreeHelp(dir, level):
	result = "|"*level + "↳Directory: " + dir[0] + "\n"
	for val in dir[1:]:
		#if type(val) is str:
		#	print(val)
		if type(val) is str:
			result += "|"*level + "↦" +  val + "\n"
		else:
			result += dispTreeHelp(val, level+1) + "\n"
	return result
	
	
#def update_tree(request):
	#newTree = ReportsTree(owner = request.user.username, treeStruct = "things")
	#newTree.save()
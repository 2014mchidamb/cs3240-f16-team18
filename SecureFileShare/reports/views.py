from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import ReportsTree
import json

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
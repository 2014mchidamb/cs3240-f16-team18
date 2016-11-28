import requests
from html.parser import HTMLParser
from Crypto.PublicKey import RSA
from Crypto import Random
import os.path

#main
base_url = "http://localhost:8000/"
login_url = base_url + "accounts/login/"

print("Welcome to the Standalone App!")

user = "nke5ka"# input("Username: ")
password = "passcode"#input("Password: ")

response = requests.get(login_url)
data = {"username": user, "password": password}

# CSRF Stuff
class CSRFGetter(HTMLParser):
	def __init__(self, dict):
		self.target = dict
		super(CSRFGetter, self).__init__()

	def handle_starttag(self, tag, attrs):
		if "csrfmiddlewaretoken" in attrs:
			self.target["csrfmiddlewaretoken"] = attrs["csrfmiddlewaretoken"]

csrf_getter = CSRFGetter(data)
csrf_getter.feed(response.text)

# login result
print(requests.post(login_url, cookies=response.cookies, data=data))

#If successful login...

#If this user has logged in before, I don't need to generate a new key.
#Check based on privateKey.pem on computer.
if(os.path.isfile('privateKey.pem')):
	#open the file, save the key
	file = open('privateKey.pem', 'r')
	#Note: this is currently the entire key with some text.
	#print(file.read())
else:
	random_generator = Random.new().read
	key = RSA.generate(1024, random_generator)
	#then store key to file on disk.
	file = open("privateKey.pem", "wb")
	file.write(key.exportKey('PEM'))
	file.close()

while (True):
	print("\nWhat would you like to do?")
	print("0. List your reports.")
	print("1. List your files and details in report.")
	print("2. Download a file.")
	print("3. Upload a file.")
	print("4. Read a private message.")
	print("9. Exit.")
	cmd = input("Enter a number corresponding to a command: ")
	if cmd == "0":
		print("Reports List:")
		dl_link = base_url + "file_list"
		response = requests.post(dl_link, data={"user": user, "report": "ALL`REP"})
		print(response.text.replace(",","\n"))
	
	elif cmd == "1":
		rep = input("What is the name of your report? ")
		print("Files List:")
		dl_link = base_url + "file_list"
		response = requests.post(dl_link, data={"user": user, "report": rep})
		print(response.text)

	elif cmd == "2":
		#load the requested item.
		dl_link = base_url + "file_get"
		needed  = input("Type in name of report: ")
		needed2 = input("Type in name of file: ")
		print("Loading file...")
		response = requests.post(dl_link, data={"user": user, "report": needed, "file": needed2})
		if response.content == "No file found within requested report.":
			print("No such file.")
			continue
		
		with open(needed2, 'wb') as f:
			f.write(response.content)
		print("Downloaded.")

	elif cmd == "3":
		#upload a response
		dl_link = base_url + "file_upload"
		needed  = input("Type in name of report: ")
		needed2  = input("Type in name of file: ")
		
		upl=os.path.basename(needed2)
		
		if not os.path.isfile(upl):
			print("No such file to upload")
			continue
		upl = {'files': open(upl,"rb")}
		
		print("Uploading file...")
		response = requests.post(dl_link, data={"rep_name":needed}, files=upl)
		print(response.content)
	elif cmd == "4":
		dl_link = base_url + "read"
		#probably not right
		needed = user
		print("Loading message...")
		response = requests.get(dl_link + '?name=' + needed)
		print(response.content)
	elif cmd == "9":
		print("Goodbye.")
		exit()
	else:
		print("Invalid command.")

import requests
from Crypto.PublicKey import RSA
from Crypto import Random

#main
base_url = "http://localhost:8000/"

print("Welcome to the Standalone App!")
user = input("Username: ")

print("<<LOGIN WILL GO HERE>>")

#If successful login...

#If this user has logged in before, I don't need to generate a new key.
random_generator = Random.new().read
key = RSA.generate(1024, random_generator)
#then store key to file on disk.
file = open("privateKey.pem", "wb")
file.write(key.exportKey('PEM'))
file.close()

while (True):
	print("\nWhat would you like to do?")
	print("1. List your files.")
	print("2. Download a response.")
	print("3. Upload a response.")
	cmd = input("Enter a number corresponding to a command: ")
	if cmd == "1":
		#Lists all the files
		print("Files List:")
		dl_link = base_url + "file_list"
		response = requests.get(dl_link)
		print(response.text)
		
	elif cmd == "2":
		#load the requested item.
		dl_link = base_url + "file_get"
		needed  = input("Type in name of response: ")
		print("Loading response...")
		response = requests.get(dl_link + '?name=' + needed)
		print(response.content)
	elif cmd == "3":
		#upload a response
		dl_link = base_url + "file_upload"
		needed  = input("Type in name of response: ")
		
		with open(needed, 'rb') as in_file:
			upload_file = in_file.read()
		
		print("Uploading response...")
		response = requests.post(dl_link, data={"name":needed, "cont":upload_file})
		#print(response.content)
	else:
		print("Invalid command. Goodbye.")
		exit()
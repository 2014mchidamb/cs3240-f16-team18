import requests

print("Welcome to the Standalone App!")
user = input("Username: ")
print("<<LOGIN WILL GO HERE>>")
while (True):
	print("\nWhat would you like to do?")
	print("1. List your files.")
	print("2. Download a file.")
	print("3. Upload a file.")
	cmd = input("Enter a number corresponding to a command: ")
	if cmd == "1":
		#Lists all the files
		print("Files List:")
		dl_link = "http://localhost:8000/file_list"
		file = requests.get(dl_link)
		print(file.text)
		
	elif cmd == "2":
		#load the requested item.
		dl_link = "http://localhost:8000/file_get"
		needed  = input("Type in name of file: ")
		print("Loading file...")
		file = requests.get(dl_link+'?name='+needed)
		print(file.content)
	elif cmd == "3":
		#upload a file
		dl_link = "http://localhost:8000/file_upload"
		needed  = input("Type in name of file: ")
		
		with open(needed, 'rb') as in_file:
			upload_file = in_file.read()
		
		print("Uploading file...")
		file = requests.post(dl_link, data={"name":needed, "cont":upload_file})
		#print(file.content)
	else:
		print("Invalid command. Goodbye.")
		exit()
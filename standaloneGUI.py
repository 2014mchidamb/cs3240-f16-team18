base_url = "http://localhost:8000/"
#base_url = "https://mighty-fjord-54317.herokuapp.com/"

import requests
from html.parser import HTMLParser
from Crypto.PublicKey import RSA
from Crypto import Random
import os.path
import getpass
import hashlib
import tkinter
from tkinter import filedialog
from tkinter import messagebox
import base64

#######Crypto Stuff Here
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import DES
from Crypto.Hash import SHA256
def encrypt_file(file_name, sym_key):
    """Encrypts file with sym_key"""
    if not isinstance(sym_key, type(b'')):
        print("Key must be in bytes")
        return False
    sym_8 = (SHA256.new(sym_key)).digest()[0:8]
    des = DES.new(sym_8, DES.MODE_ECB)
    try:
        with open(file_name, 'rb') as in_file:
            out_name = file_name + ".enc"
            with open(out_name, 'wb') as out_file:
                next_chunk = in_file.read(8)
                while True:
                    chunk = next_chunk
                    next_chunk = in_file.read(8)
                    if next_chunk:
                        chunk = des.encrypt(chunk)
                        out_file.write(chunk)
                    else:
                        to_fill = 8-len(chunk)
                        if to_fill is 0:
                            chunk = des.encrypt(chunk)
                            out_file.write(chunk)
                            chunk = des.encrypt(b'10000000')
                            out_file.write(chunk)
                        else:
                            # Pad with 1 then 0s
                            chunk += b'1'
                            for i in range(to_fill-1):
                                chunk += b'0'
                            chunk = des.encrypt(chunk)
                            out_file.write(chunk)
                            chunk = des.encrypt(b'00000000')
                            out_file.write(chunk)
                        break
    except FileNotFoundError:
        print("Files could not be opened.  Check your spelling.")
        return False
    return True


def decrypt_file(file_name, sym_key):
    """Decrypts file using sym_key"""
    if not isinstance(sym_key, type(b'')):
        print("Key must be in bytes")
        return False
    try:
        sym_8 = (SHA256.new(sym_key)).digest()[0:8]
        des = DES.new(sym_8, DES.MODE_ECB)
        if len(file_name) < 5 or file_name[-4:] != ".enc":
            print("Not an encoded file")
            return False
        with open(file_name, 'rb') as in_file:
            out_name = file_name[:-4]
            with open(out_name, 'wb') as out_file:
                next_chunk = in_file.read(8)
                next_next_chunk = in_file.read(8)
                while True:
                    chunk = next_chunk
                    next_chunk = next_next_chunk
                    next_next_chunk = in_file.read(8)
                    if next_next_chunk:
                        chunk = des.decrypt(chunk)
                        out_file.write(chunk)
                        #print(chunk)
                    else:
                        # Last chunk is empty, second to last is
                        # sentinel and is dropped
                        indicator_chunk = des.decrypt(next_chunk)
                        chunk = des.decrypt(chunk)
                        if indicator_chunk != b'10000000':
                            end_one = chunk.rfind(b"1")
                            chunk = chunk[:end_one]
                        out_file.write(chunk)
                        #print(chunk)
                        break
    except FileNotFoundError:
        print("Files could not be opened.  Check your spelling.")
        return False
    return True

def get_hash(file_name):
	try:
		hashy = hashlib.md5()
		with open(file_name, 'rb') as in_file:
			hashy.update(in_file.read())
		return base64.b64encode(hashy.digest())
			
	except FileNotFoundError:
		print("Files could not be opened.  Check your spelling.")
		return ""



#main
login_url = base_url + "fda_login"

print("Welcome to the Standalone App!")

while(True):
	user = input("Username: ")
	password = getpass.getpass("Password: ")

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
	#resp = (requests.post(login_url, cookies=response.cookies, data=data))

	response = requests.post(login_url, data=data)
	#print(response)
	#print(response.content)

	if response.content != b"SUCCESS":
		print("Incorrect Login Information. Try again.")
	else:
		print("Welcome, ", user, "!", sep="")
		break



class App:
	def OnDouble(self, event):
		clicked = event.widget
		selected = clicked.curselection()
		self.nameOfRep = clicked.get(selected[0])
		colon=self.nameOfRep.find(':')
		self.nameOfRep = self.nameOfRep[0:colon]
		print(self.nameOfRep)
		dl_link = base_url + "desc_get"
		response = requests.post(dl_link, data={"user": user, "report": self.nameOfRep})
		print (response.text)
		self.descr.delete("1.0", tkinter.END)
		self.descr.insert(tkinter.END, response.text)
		dl_link = base_url + "file_list"
		response = requests.post(dl_link, data={"user": user, "report": self.nameOfRep})
		print(response.text)
		results = response.text[1:-1]
		listFiles = results.split(",")
		print(listFiles)
		self.listOfFiles.delete(0,tkinter.END)
		for i in listFiles:
			self.listOfFiles.insert(tkinter.END,i.strip().replace("'",""))
		self.listOfFiles.bind("<Double-Button-1>", self.OnFileDouble)
		self.fileName.delete("1.0",tkinter.END)
	
	def OnFileDouble(self, event):
		clicked = event.widget
		selected = clicked.curselection()
		nameOfFile = clicked.get(selected[0])
		
		self.fileName.delete("1.0",tkinter.END)
		self.fileName.insert(tkinter.END,nameOfFile)

	def download(self, event):
		#load the requested item.
		dl_link = base_url + "file_get"
		if self.nameOfRep is None:
			return
		needed  = self.nameOfRep
		needed2 = self.fileName.get("1.0",tkinter.END).strip()
		print(needed,needed2)
		print("Loading file...")
		response = requests.post(dl_link, data={"user": user, "report": needed, "file": needed2})
		if response.content == b"No file found within requested report.":
			print("No such file.")
			return
		
		with open(needed2, 'wb') as f:
			f.write(response.content)
		print("Downloaded.")
		if ".enc" in needed2:
			#dec_it = input("This file is encrypted.  Do you want to unencrypt? (y to do so)")
			#if dec_it == "y": decrypt_file(needed2, str.encode(password))
			dec_it = messagebox.askquestion("This file is encrypted.", "Do you want to unencrypt?", icon='warning')
			if dec_it == 'yes':
				decrypt_file(needed2, str.encode(password))
	
	def upload(self, event):
		dl_link = base_url + "file_upload"
		needed  = self.nameOfRep
		newroot = tkinter.Tk()
		newroot.withdraw()
		needed2 = filedialog.askopenfilename()
		print(needed,needed2)
		
		upl=os.path.abspath(needed2)
		
		if not os.path.isfile(upl):
			print("No such file to upload")
			return
		
		hashy = get_hash(upl)
		print("Hash of uploaded file is:",hashy)
		
		encrypt_file(needed2, str.encode(password))
		
		upl=os.path.abspath(needed2+".enc")
		
		upl = {'files': open(upl,"rb")}
		
		print("Uploading file...")
		response = requests.post(dl_link, data={"rep_name":needed, "hashy": hashy}, files=upl)
		print(response.content)
	
	def verify(self, event):
		print("Verifying...")
		dl_link = base_url + "file_verify"
		needed  = self.nameOfRep
		needed2 = self.fileName.get("1.0",tkinter.END).strip().replace(".enc", "")
		hashy = get_hash(needed2)
		if hashy == "":
			return
		response = requests.post(dl_link, data={"user": user, "report": needed, "file": needed2})
		if response.content == b"No file found within requested report.":
			print("No such file.")
			return
		print(response.content, hashy)
		if response.content == hashy:
			dec_it = messagebox.askquestion("This file was not changed", "There are no changes.", icon='warning')
		else:
			dec_it = messagebox.askquestion("This file was altered!", "There were changes made!", icon='warning')
		
	def __init__(self):
		root = tkinter.Tk("File Download Application")
		root.minsize(400,600);

		selectFrame = tkinter.Frame(root)
		selectFrame.pack()
		scroll = tkinter.Scrollbar(selectFrame)
		scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)

		listOfReports = tkinter.Listbox(selectFrame, width=100)
		listOfReports.grid_propagate(0)
		

		dl_link = base_url + "file_list"
		response = requests.post(dl_link, data={"user": user, "report": "ALL`REP"})
		results = response.text[1:-1]
		print(results)
		listReps = results.split(",")
		print(listReps)
		for i in listReps:
			listOfReports.insert(tkinter.END,i.strip())
		listOfReports.bind("<Double-Button-1>", self.OnDouble)

		listOfReports.config(yscrollcommand=scroll.set)
		scroll.config(command=listOfReports.yview)
		listOfReports.pack()
		
		textThing = tkinter.Label(root, text="REPORT SUMMARY")
		textThing.pack()
		
		self.descr = tkinter.Text(root, height=5, width=50)
		self.descr.pack()
		self.descr.insert(tkinter.END, "Click to select a report.")
		
		textThing = tkinter.Label(root, text="FILES AVAILABLE FOR DOWNLOAD")
		textThing.pack()
		
		selectFileFrame = tkinter.Frame(root)
		selectFileFrame.pack()
		scrollFile = tkinter.Scrollbar(selectFileFrame)
		scrollFile.pack(side=tkinter.RIGHT, fill=tkinter.Y)

		self.listOfFiles = tkinter.Listbox(selectFileFrame, width=100)
		self.listOfFiles.grid_propagate(0)
		#ADD STUFF HERE
		#listOfFiles.bind("<Double-Button-1>", self.OnFileDouble)

		self.listOfFiles.config(yscrollcommand=scroll.set)
		scrollFile.config(command=self.listOfFiles.yview)
		self.listOfFiles.pack()
		
		textThing = tkinter.Label(root, text="FILE CURRENTLY SELECTED")
		textThing.pack()
		
		self.fileName = tkinter.Text(root, height=1, width=50)
		self.fileName.pack()
		self.fileName.insert(tkinter.END, "No file selected")
		
		dlButton = tkinter.Button(root, text="DOWNLOAD")
		dlButton.bind("<Double-Button-1>", self.download)
		dlButton.pack()
		
		ulButton = tkinter.Button(root, text="UPLOAD")
		ulButton.bind("<Double-Button-1>", self.upload)
		ulButton.pack()
		
		vButton = tkinter.Button(root, text="VERIFY")
		vButton.bind("<Double-Button-1>", self.verify)
		vButton.pack()
		
		root.mainloop()
		
app=App()



	
	# elif cmd == "3":
		# #upload a response
		
	# elif cmd == "4":
		# dl_link = base_url + "file_verify"
		# needed  = input("Type in name of report: ")
		# needed2 = input("Type in name of file: ")
		# hashy = get_hash(needed2)
		# if hashy == "":
			# continue
		# response = requests.post(dl_link, data={"user": user, "report": needed, "file": needed2})
		# if response.content == b"No file found within requested report.":
			# print("No such file.")
			# continue
		# print(response.content, hashy)
		# if response.content == hashy:
			# print("Files match.")
		# else:
			# print("Files were altered during transit.")
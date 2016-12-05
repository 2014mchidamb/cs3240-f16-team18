import requests
from html.parser import HTMLParser
from Crypto.PublicKey import RSA
from Crypto import Random
import os.path
import getpass
import hashlib



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
		return hashy.digest()
			
	except FileNotFoundError:
		print("Files could not be opened.  Check your spelling.")
		return ""



#main
base_url = "http://localhost:8000/"
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

#If successful login...


#If this user has logged in before, I don't need to generate a new key.
#Check based on privateKey.pem on computer.
#if(os.path.isfile('privateKey.pem')):
	#open the file, save the key
	#file = open('privateKey.pem', 'r')
	#Note: this is currently the entire key with some text.
	#print(file.read())
#else:
if(True):
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
	print("4. Verify file integrity.")
	#print("5. Read a private message.")
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
		if response.content == b"No file found within requested report.":
			print("No such file.")
			continue
		
		with open(needed2, 'wb') as f:
			f.write(response.content)
		print("Downloaded.")
		if ".enc" in needed2:
			dec_it = input("This file is encrypted.  Do you want to unencrypt? (y to do so)")
			if dec_it == "y": decrypt_file(needed2, str.encode(password))

	elif cmd == "3":
		#upload a response
		dl_link = base_url + "file_upload"
		needed  = input("Type in name of report: ")
		needed2  = input("Type in name of file: ")
		
		upl=os.path.basename(needed2)
		
		if not os.path.isfile(upl):
			print("No such file to upload")
			continue
		
		hashy = get_hash(upl)
		print("Hash of uploaded file is:",hashy)
		
		encrypt_file(needed2, str.encode(password))
		
		upl=os.path.basename(needed2+".enc")
		
		upl = {'files': open(upl,"rb")}
		
		print("Uploading file...")
		response = requests.post(dl_link, data={"rep_name":needed, "hashy": hashy}, files=upl)
		print(response.content)
	elif cmd == "4":
		dl_link = base_url + "file_verify"
		needed  = input("Type in name of report: ")
		needed2 = input("Type in name of file: ")
		hashy = get_hash(needed2)
		if hashy == "":
			continue
		response = requests.post(dl_link, data={"user": user, "report": needed, "file": needed2})
		if response.content == b"No file found within requested report.":
			print("No such file.")
			continue
		print(response.content, hashy)
		if response.content == hashy:
			print("Files match.")
		else:
			print("Files were altered during transit.")
	elif cmd == "5NOPE":#Change back to just 5 if reimplemented
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
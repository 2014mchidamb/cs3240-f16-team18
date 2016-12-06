import requests
from html.parser import HTMLParser
from Crypto.PublicKey import RSA
from Crypto import Random
import os.path
import getpass
import hashlib
import base64
import cryptography
import cryptography.hazmat
import cryptography.hazmat.backends
import cryptography.hazmat.bindings
import cryptography.hazmat.primitives
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from base64 import b64encode, b64decode



#######Crypto Stuff Here
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import DES
from Crypto.Hash import SHA256
def encrypt_file(file_name):
	"""Encrypts file symmetrically"""
	try:
		key = Fernet.generate_key()
		f = Fernet(key)
		with open(file_name, "rb") as in_file:
			token = f.encrypt(in_file.read())
			with open(file_name + ".enc") as out_file:
				out_file.write(token)
	except FileNotFoundError:
		print("Files could not be opened.  Check your spelling.")
		return None
	return key


def decrypt_file(file_name, sym_key):
	"""Decrypts file using sym_key"""
	if not isinstance(sym_key, type(b'')):
		print("Key must be in bytes")
		return False
	try:
		f = Fernet(sym_key)
		with open(file_name, "rb") as in_file:
			token = f.decrypt(in_file.read())
			with open(file_name[:-4], "wb") as out_file:
				out_file.write(token)
	except FileNotFoundError:
		print("Files could not be opened.  Check your spelling.")
		return False
	return True

def get_hash(file_name):
	try:
		hashy = hashlib.sha512()
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

private_key = None
key_filename = user + ".pem"

if os.path.isfile(key_filename):
	with open(key_filename, "rb") as key_file:
		private_key = serialization.load_pem_private_key(
			key_file.read(),
			password=password,
			backend=default_backend()
		)

if private_key is None: # generate and save key
	private_key = rsa.generate_private_key(
		public_exponent = 65537,
		key_size = 2048,
		backend = default_backend()
	)
	pem = private_key.private_bytes(
		encoding = serialization.Encoding.PEM,
		format = serialization.PrivateFormat.PKCS8,
		encryption_algorithm = serialization.BestAvailableEncryption(password.encode())
	)
	with open(key_filename, "wb") as key_file:
		key_file.write(pem)

public_key = private_key.public_key()
# TODO: Publish public key to keyserver


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
			if dec_it == "y":
				response = requests.post(base_url + "get_filekey", data={"public_key": public_key, "file": needed2})
				decrypt_file(needed2, response.content)

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
		print("Hash of uploaded file is:",base64.b64encode(hashy))

		symmetric_key = encrypt_file(needed2, str.encode(password))
		encrypted_symmetric_key = public_key.encrypt(
			symmetric_key,
			padding.OAEP(
				mgf=padding.MGF1(algorithm=hashes.SHA512()),
				algorithm=hashes.SHA512(),
				label=None
			)
		)

		upl=os.path.basename(needed2+".enc")

		upl = {'files': open(upl,"rb")}

		print("Uploading file...")
		response = requests.post(dl_link, data={"rep_name":needed, "hashy": base64.b64encode(hashy)}, files=upl, file_key=b64encode(encrypted_symmetric_key))
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
		if base64.b64decode(response.content) == hashy:
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
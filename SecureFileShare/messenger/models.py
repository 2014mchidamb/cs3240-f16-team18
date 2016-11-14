from django.contrib.auth.models import User
from django.db import models
from Crypto.PublicKey import RSA
from Crypto import Random

# Create your models here.
class Message(models.Model):
    text = models.TextField(max_length=500, blank=True)
    sender = models.TextField(max_length=500, blank=True)
    recipient = models.TextField(max_length=500, blank=True)
    encryptedFlag = models.BooleanField(default=False)

def getKey():
    # note: probably shouldn't be creating a public key every time.
    #It should just be created once upon loading, or one key should be
    # added to the database. Then it's retrieved.
    random_generator = Random.new().read
    key = RSA.generate(1024, random_generator)
    return key

def enc(message):
    message.encryptedFlag = True
    key = getKey()
    public_key = key.publickey()
    enc_data = public_key.encrypt(message, 32)
    return enc_data

def dec(message):
    message.encryptedFlag = False
    key = getKey()
    return key.decrypt(message)


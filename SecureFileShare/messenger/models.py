from django.contrib.auth.models import User
from django.db import models
from Crypto.PublicKey import RSA
from Crypto import Random

# Create your models here.
class Message(models.Model):
    text = models.TextField(max_length=500, blank=True)
    sender = models.OneToOneField(User, on_delete=models.Profile)
    recipient = models.OneToOneField(User, on_delete=models.Profile)
    encryptedFlag = models.BooleanField(default=False)

def enc(message):
    #note: probably shouldn't be creating a public key every time.
    random_generator = Random.new().read
    key = RSA.generate(1024, random_generator)
    public_key = key.publickey()
    enc_data = public_key.encrypt('abcdefgh', 32)
    message.encryptedFlag = True


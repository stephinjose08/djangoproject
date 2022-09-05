from concurrent.futures import process
import os
from twilio.rest import Client
from django.conf import settings
from django.contrib import messages
from dotenv import load_dotenv

load_dotenv()

account_sid = settings.ACCOUNT_SID
auth_token = settings.AUTH_TOKEN
client = Client(account_sid, auth_token)
def send_sms(phone_number):
    verification = client.verify \
                        .v2 \
                        .services(settings.SERVICES) \
                        .verifications \
                        .create(to=f'+91{phone_number}', channel='sms')

    print(verification.status)
  


account_sid = settings.ACCOUNT_SID
auth_token = settings.AUTH_TOKEN
client = Client(account_sid, auth_token)
def check_sms(user,number):
        verification_check = client.verify \
                                    .v2 \
                                    .services(settings.SERVICES) \
                                    .verification_checks \
                                    .create(to=f'+91{user}', code=number)
            
       
        return(verification_check.status)
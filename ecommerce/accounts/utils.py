import os
from twilio.rest import Client
from django.conf import settings

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure

# account_sid = 'ACec5b967dd33bfb87b6b5bee530d75fcf'
# auth_token = '5d44f04a4024d09709b4029b76305c4c'
# client = Client(account_sid, auth_token)

# def send_sms(phone_number):
#     message = client.messages.create(
#                         body=f'your varification code is ',
#                         from_='+17752043347',
#                         to=f'+91{phone_number}'
#                     )
#     print(message.sid)

# import os
# from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = settings.account_sid
auth_token = settings.auth_token
client = Client(account_sid, auth_token)
def send_sms(phone_number):
    verification = client.verify \
                        .v2 \
                        .services(settings.services) \
                        .verifications \
                        .create(to=f'+91{phone_number}', channel='sms')

    print(verification.status)



account_sid = settings.account_sid
auth_token = settings.auth_token
client = Client(account_sid, auth_token)
def check_sms(user,number):
        verification_check = client.verify \
                                    .v2 \
                                    .services(settings.services) \
                                    .verification_checks \
                                    .create(to=f'+91{user}', code=number)

        print(verification_check.status)
        return(verification_check.status)
import os
from twilio.rest import Client


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
account_sid = 'ACec5b967dd33bfb87b6b5bee530d75fcf'
auth_token = 'c66192b9907fcdb92a5d57c5ab287ec0'
client = Client(account_sid, auth_token)
def send_sms(phone_number):
    verification = client.verify \
                        .v2 \
                        .services('VAbfb48002429d46cce03609faf15e559e') \
                        .verifications \
                        .create(to=f'+91{phone_number}', channel='sms')

    print(verification.status)



account_sid = 'ACec5b967dd33bfb87b6b5bee530d75fcf'
auth_token = 'c66192b9907fcdb92a5d57c5ab287ec0'
client = Client(account_sid, auth_token)
def check_sms(user,number):
        verification_check = client.verify \
                                    .v2 \
                                    .services('VAbfb48002429d46cce03609faf15e559e') \
                                    .verification_checks \
                                    .create(to=f'+91{user}', code=number)

        print(verification_check.status)
        return(verification_check.status)
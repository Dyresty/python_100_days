#SMTP - Simple Mail Transfer Protocol
# Contains all the rules that determine how the mail is received by the  mail server and passed on to the next mail server
# and how mail can be sent around the internet

#TLS - Transport Layer Security. Secure connection. Encryption
#SMTP - Simple Mail Transfer Protocol
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

my_email = os.getenv("MY_EMAIL")
password = os.getenv("PASSWORD")
to_email = os.getenv("RECEIVER")

connection = smtplib.SMTP("smtp.gmail.com")
connection.starttls()
connection.login(user=my_email, password=password)
connection.sendmail(from_addr=my_email, to_addrs=to_email, 
                    msg="Subject: Hello\n\nHi Rochan,\nI hope you have a great day ahead.\n\nBest Regards\nRochan Kumar Saravanakannan")
connection.close()



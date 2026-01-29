from pathlib import Path
from dotenv import load_dotenv
import datetime as dt
import os
import random 
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


load_dotenv()

my_email = os.getenv("MY_EMAIL")
password = os.getenv("PASSWORD")
to_email = os.getenv("RECEIVER3")

SCRIPT_DIR = Path(__file__).parent

try:
    with open(str(SCRIPT_DIR / 'quotes left.txt'), 'r', encoding='utf-8') as file:
        quotes = file.readlines()
except:
    with open(str(SCRIPT_DIR / 'quotes.txt'), 'r', encoding='utf-8') as file:
        quotes = file.readlines()

# Remove newline characters from each quote
quotes = [quote.strip() for quote in quotes]

i = random.randint(0,len(quotes))
now = dt.datetime.now()

if now.weekday() == 3:
    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(user=my_email, password=password)
    
    # Create MIME message for UTF-8 support
    msg = MIMEMultipart()
    msg["From"] = my_email
    msg["To"] = to_email
    msg["Subject"] = "Motivation Friday"
    
    body = f"Hi Nanditha,\n\nI hope you have a great week ahead.\n\n{quotes[i]}\n\nBest Regards\nRochan Kumar Saravanakannan"
    msg.attach(MIMEText(body, "plain", "utf-8"))
    
    connection.sendmail(from_addr=my_email, to_addrs=to_email, msg=msg.as_string())
    connection.close()
    quotes.remove(quotes[i])
    with open(str(SCRIPT_DIR / 'quotes left.txt'), 'w', encoding='utf-8') as file:
        for quote in quotes:
            file.write(quote + '\n')



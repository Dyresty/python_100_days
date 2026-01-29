from pathlib import Path
from dotenv import load_dotenv
import datetime as dt
import os
import random 
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SCRIPT_DIR = Path(__file__).parent
load_dotenv()

my_email = os.getenv("MY_EMAIL")
password = os.getenv("PASSWORD")

recipients_list = []
recipients_file = SCRIPT_DIR / "data.json"

if recipients_file.exists():
    try:
        with open(recipients_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            for name, info in data.items():
                email_addr = info.get("email")
                if email_addr:
                    recipients_list.append((name, email_addr))
    except Exception as e:
        print(f"Error reading JSON: {e}")

if not recipients_list:
    env_receiver = os.getenv("RECEIVER")
    if env_receiver:
        recipients_list.append(("Friend", env_receiver))

quotes_path = SCRIPT_DIR / 'quotes left.txt'
if not quotes_path.exists() or quotes_path.stat().st_size == 0:
    quotes_path = SCRIPT_DIR / 'quotes.txt'

try:
    with open(quotes_path, 'r', encoding='utf-8') as file:
        quotes = [line.strip() for line in file if line.strip()]
except FileNotFoundError:
    quotes = ["Keep going! You're doing great."]

now = dt.datetime.now()

if now.weekday() == 3 and quotes:
    random_index = random.randint(0, len(quotes) - 1)
    selected_quote = quotes[random_index]

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)

            for name, addr in recipients_list:
                try:
                    msg = MIMEMultipart()
                    msg["From"] = my_email
                    msg["To"] = addr
                    msg["Subject"] = "Monday Motivation"

                    body = f"Hi {name},\n\nI hope you have a great week ahead.\n\n{selected_quote}\n\nBest Regards,\nRochan Kumar Saravanakannan"
                    msg.attach(MIMEText(body, "plain", "utf-8"))
                    
                    connection.send_message(msg)
                    print(f"Successfully sent to {name} at {addr}")
                except Exception as e:
                    print(f"Failed to send to {addr}: {e}")

        quotes.pop(random_index)
        with open(SCRIPT_DIR / 'quotes left.txt', 'w', encoding='utf-8') as file:
            file.write("\n".join(quotes))

    except Exception as e:
        print(f"SMTP Connection Error: {e}")
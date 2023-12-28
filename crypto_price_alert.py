import requests
import os 
import smtplib
from email.mime.text import MIMEText

SMTP_EMAIL = os.environ.get("SMTP_EMAIL")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")

def send_email(to_address, subject, body):
    SMTP_PORT = 587
    SMTP_SERVER = "smtp.gmail.com"

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SMTP_EMAIL, SMTP_PASSWORD)

    message = MIMEText(body)
    message['Subject'] = subject
    message['From'] = SMTP_EMAIL
    message['To'] = to_address

    server.sendmail(SMTP_EMAIL, to_address, message.as_string())
    server.quit()


def get_crypto(symbol):
    api_url = f'https://api.coincap.io/v2/assets/{symbol}'
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()['data']
    except requests.exceptions.RequestException as e:
        return None

def main():
    target_price = 40000
    crypto = get_crypto('bitcoin')
    to_email = "recipient@mail.com"
    subject = "Crypto Price Alert"

    if crypto is not None:
        if float(crypto['priceUsd']) > target_price:
            body = f"The Current Price for {crypto['name']} is {crypto['priceUsd']} USD"
            send_email(to_email, subject, body)
import os 
import smtplib
import requests 
from bs4 import BeautifulSoup

product_url = 'https://www.amazon.co.uk/FINIS-Long-Floating-Fins-Black/dp/B001M0O4Y0'
threshold = 25

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive', 
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
}

GMAIL_ADDRESS = os.environ['GMAIL_ADDRESS']
PASSWORD = os.environ['GMAIL_PASSWORD']

def get_price(): 
    response = requests.get(product_url, headers=HEADERS)
    if response.status_code == 200: 
        soup = BeautifulSoup(response.content, 'html.parser')                   # Might need to switch to 'lxml' as the parser
        price_block = soup.find('table', class_='a-lineitem a-align-top')
        price = min([float(price.get_text().replace('£', '')) for price in price_block.find_all('span', class_='a-offscreen')])
        return price 

def send_email_notification(): 
    alert_text = f'The price of your watched product: {product_url} \n is now less than {threshold} quid. Go buy it now!'
    with smtplib.SMTP('smtp.gmail.com') as connection: 
        connection.starttls()
        connection.login(GMAIL_ADDRESS, PASSWORD)
        connection.sendmail(
            from_addr=GMAIL_ADDRESS, 
            to_addrs='mariasmickersgill@live.com', 
            msg=f'Subject: Amazon Price Alert! \n\n{alert_text}'
        )

if get_price() < threshold: 
    send_email_notification()
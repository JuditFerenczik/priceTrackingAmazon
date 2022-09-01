import requests
from bs4 import BeautifulSoup
import lxml
import smtplib
from secretkeys import PASSWORD,MY_EMAIL, TO_MY_EMAIL
#URL = "https://www.amazon.de/Eono-Amazon-Kleidertaschen-Verpackungsw%C3%BCrfel-Kofferorganizer/dp/B07ZT4P357/ref=asc_df_B07ZT4P357/?tag=&linkCode=df0&hvadid=411881727593&hvpos=&hvnetw=g&hvrand=14182401356872766304&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=20228&hvtargid=pla-889363882444&th=1&ref=&adgrpid=91215672938"
URL = input("The product you would like to buy from amazon.de:")
try:
    limit_price = float(input("Enter the highest price what is acceptable! "))
    headers = {
        "Content-Type": "text",
        "Accept-Language": "en-US,en;q=0.9,hu-HU;q=0.8,hu;q=0.7,de;q=0.6",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
    }
    r = requests.get(URL, headers=headers)
    r.raise_for_status()
    website_html = r.text
    soup = BeautifulSoup(website_html, "lxml")

    price = soup.select("span.apexPriceToPay > span.a-offscreen")
    if len(price) == 0:
        price = soup.select("span.priceToPay > span.a-offscreen")
    price = float(price[0].getText().split("€")[0].replace(",", "."))
    print(price)
    if price <= limit_price:
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:  # smtp.mail.yahoo.com
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=TO_MY_EMAIL,
                msg=f"Subject:Hello\n\nThe price of the chosen product decreased to {price}.")
            print("E-mail sent successfully!")

except:
    print("The type of the input value is not float!!")

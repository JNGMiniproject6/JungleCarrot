from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_coupang(url):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    og_title = soup.find("meta", property="og:title")['content']
    prod_image_detail = soup.find("div", class_="prod-image__detail")
    total_price = soup.find("span", class_="total-price")

    return og_title, prod_image_detail, total_price

def scrape_naver_smartstore(url):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    info_1 = soup.find("div", class_="_22kNQuEXmb _copyable")
    info_2 = soup.find("div", class_="bd_1uFKu")
    info_3 = soup.find("div", class_="_1LY7DqCnwR")

    return info_1, info_2, info_3

@app.route('/api/site_scraping')
def index():
    url = "https://www.coupang.com/vp/products/335833200?itemId=17982326014&vendorItemId=85139110125&pickType=COU_PICK&q=%EA%B3%A0%EC%96%91%EC%9D%B4&itemsCount=36&searchId=170c23c33ddc475a8a994d1960670660&rank=1&isAddedCart="
    site_identifier = url.split('/')[2]

    if site_identifier == "www.coupang.com":
        og_title, prod_image_detail, total_price = scrape_coupang(url)
        return render_template('coupang.html', og_title=og_title, prod_image_detail=prod_image_detail, total_price=total_price)

    elif site_identifier == "smartstore.naver.com":
        info_1, info_2, info_3 = scrape_naver_smartstore(url)
        return render_template('naver_smartstore.html', info_1=info_1, info_2=info_2, info_3=info_3)

    else:
        return "Unsupported site"

if __name__ == '__main__':
    app.run(debug=True)

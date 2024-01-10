import requests
from bs4 import BeautifulSoup

url = "https://www.coupang.com/vp/products/335833200?itemId=17982326014&vendorItemId=85139110125&pickType=COU_PICK&q=%EA%B3%A0%EC%96%91%EC%9D%B4&itemsCount=36&searchId=170c23c33ddc475a8a994d1960670660&rank=1&isAddedCart="

# URL 첫 번째 단어 추출
site_identifier = url.split('/')[2]

# 각 사이트에 따라 다르게 처리
if site_identifier == "www.coupang.com":
    # 쿠팡 스크래핑 코드
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    og_title = soup.find("meta", property="og:title")['content']
    prod_image_detail = soup.find("div", class_="prod-image__detail")
    total_price = soup.find("span", class_="total-price")

    print(f"og:title: {og_title}")
    print(f"prod-image__detail: {prod_image_detail}")
    print(f"total-price: {total_price}")

elif site_identifier == "smartstore.naver.com":
    # 네이버 스마트스토어 스크래핑 코드
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    info_1 = soup.find("div", class_="_22kNQuEXmb _copyable")
    info_2 = soup.find("div", class_="bd_1uFKu")
    info_3 = soup.find("div", class_="_1LY7DqCnwR")

    print(f"Info 1: {info_1}")
    print(f"Info 2: {info_2}")
    print(f"Info 3: {info_3}")

else:
    print("Unsupported site")


import requests
from bs4 import BeautifulSoup
import re
import json


# 目标网页URL
def get_current_price(country_codes):
    price_list = {}
    for country_code in country_codes:
        url = "https://help.netflix.com/en/node/24926/" + country_code

        # 向URL发起请求
        response = requests.get(url)
        # print(country_code)
        # 检查请求是否成功
        if response.status_code == 200:
            try:
                soup = BeautifulSoup(response.text, "html.parser")
                # 使用CSS选择器来查找目标元素
                target = soup.select_one(
                    "body > div.global-container > div.global-content > div > div.pane-wrapper > div > div.left-pane > section.kb-article.kb-article-variant.gradient > div > div > div:nth-child(3) > ul > li:nth-child(3) > p > strong"
                )
                target = target.next_sibling
                raw_text = target.get_text()
                price = re.sub(r"[^\d.,]", "", raw_text)
                price_list[country_code] = price
            except AttributeError:
                continue
        else:
            print("网页请求失败。")
    return price_list


def get_country_codes():
    with open("country_codes.txt", "r", encoding="utf-8") as f:
        country_codes = f.readlines()[0].split(",")
        return country_codes


def comparison(prev_price_list, cur_price_list):
    msg = ""
    if prev_price_list == cur_price_list:
        msg += "Previous price list is equal to current price list"
    else:
        msg += "List of different price:"
        for key, value in prev_price_list.items():
            if value != cur_price_list[key]:
                msg += "\nPrice of {} is different.".format(key) + " Fuck you Netflix!!"

    return msg


def sendMSG(token, msg):

    debugMode = False
    if debugMode:
        print(msg)
    else:
        url = "https://api.telegram.org/bot{}/sendMessage".format(token)
        payload = {
            "chat_id": -1002141784679,
            "text": msg,
        }
        res = requests.post(url, data=payload)


if __name__ == "__main__":
    country_codes = get_country_codes()
    price_list = get_current_price(country_codes)

    with open("price_list.json", "r", encoding="utf-8") as f:
        prev_price_list = json.load(f)

    msg = comparison(prev_price_list, price_list)
    token = "7126273264:AAEp8rp1-mBzd8XYknIVWb9sPKdy8VwJMiY"
    sendMSG(token, c_id, msg)

    with open("price_list.json", "w", encoding="utf-8") as f:
        json.dump(price_list, f, ensure_ascii=False, indent=4)

import json
import re
from urllib.parse import urlencode

import requests
from lxml import etree

from utils import get_html_body, get_html_template


class Investing():
    def __init__(self, symbol_url: str):
        self.symbol_url = symbol_url
        self.ses = requests.session()
        self.headers = {
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7'
        }
        self.response = self.ses.get(self.symbol_url, headers=self.headers).text
        self.pair_id = re.findall(r"window\.instrumentPopupParams\['(\d+?)'\]", self.response)[0]
        self.sml_id = re.findall(r"window.siteData.smlID = (\d+?);", self.response)[0]

    def __get_data__(self, html):
        try:
            historic_data_list = []
            response_html = etree.HTML(html)
            for data in response_html.xpath('//*[@id="curr_table"]/tbody/tr'):
                td_list = data.xpath("td")
                historic_data_list.append(
                    {
                        "date": td_list[0].text,
                        "close": td_list[1].text,
                        "open": td_list[2].text,
                        "high": td_list[3].text,
                        "low": td_list[4].text,
                        "vol": td_list[5].attrib["data-real-value"],
                        "change": td_list[6].text,
                    }
                )
            return historic_data_list
        except:
            return []

    def get_historic_data(self):
        return self.__get_data__(self.response)

    def get_historic_data_by_range(self, st_date: str, end_date: str):
        url = "https://cn.investing.com/instruments/HistoricalDataAjax"

        # payload = 'curr_id=6408&smlID=1159963&st_date=2021%2F08%2F19&end_date=2021%2F08%2F21&interval_sec=Daily&sort_col=date&sort_ord=DESC&action=historical_data'
        payload = {
            "curr_id": self.pair_id,
            "smlID": self.sml_id,
            "st_date": st_date,
            "end_date": end_date,
            "interval_sec": "Daily",
            "sort_col": "date",
            "sort_ord": "DESC",
            "action": "historical_data"
        }
        headers = {
            'authority': 'cn.investing.com',
            'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
            'accept': 'text/plain, */*; q=0.01',
            'content-type': 'application/x-www-form-urlencoded',
            'x-requested-with': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
            'sec-ch-ua-platform': '"Windows"',
            'origin': 'https://cn.investing.com',
        }
        response = requests.post(url, headers=headers, data=urlencode(payload)).text
        return self.__get_data__(response)


def get_symbol_url(symbol):
    try:
        url = "https://cn.investing.com/search/service/searchTopBar"
        payload = f'search_text={symbol}'
        headers = {
            'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'content-type': 'application/x-www-form-urlencoded',
            'x-requested-with': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
            'sec-ch-ua-platform': '"Windows"',
            'origin': 'https://cn.investing.com',
            'accept-language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7',
        }

        response = requests.post(url, headers=headers, data=payload).json()

        if len(response["quotes"]) > 0:
            return response["quotes"][0]["link"]
        else:
            raise Exception("not found data")
    except:
        return None


def main():
    for search_symbol in ["AAPL", "SPY", "TSLA", "QQQ", "MSFT"]:
        info_url = get_symbol_url(search_symbol)
        if not info_url:
            continue
        symbol = Investing(f"https://cn.investing.com{info_url}-historical-data")
        historic_data = symbol.get_historic_data()
        print(f"Q1-2: {search_symbol} Historic Data Price List\n{json.dumps(historic_data)}")
        start_date = "2021/08/19"
        end_date = "2021/09/10"
        historic_range_data = symbol.get_historic_data_by_range(start_date, end_date)
        print(
            f"Q1-3: {search_symbol} Historic Data Price List From {start_date} to {end_date}\n{json.dumps(historic_range_data)}")

        print(f"Generate {search_symbol} Historic Data HTML")
        f = open(f"{search_symbol}_Historic_Data.html", "w", encoding="utf-8")
        f.write(get_html_template(get_html_body(historic_data)))
        f.close()
        print(f"Finish Generate {search_symbol} Historic Data HTML")

        print(f"Generate {search_symbol} Historic Data HTML From {start_date} to {end_date}")
        r = open(f"{search_symbol}_Historic_Data_{start_date.replace('/', '')}_{end_date.replace('/', '')}.html", "w",
                 encoding="utf-8")
        r.write(get_html_template(get_html_body(historic_range_data)))
        r.close()
        print(f"Finish Generate {search_symbol} Historic Data HTML From {start_date} to {end_date}")


if __name__ == '__main__':
    main()

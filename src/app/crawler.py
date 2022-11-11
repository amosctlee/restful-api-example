import re
from typing import Union
import json
from zoneinfo import ZoneInfo
from datetime import datetime
import requests

from schemas.products import ProductSchema


def get_iphone14_page_n(page_num: int) -> dict:

    dt = datetime.now(tz=ZoneInfo('Asia/Taipei'))
    timestamp = int(dt.timestamp() * 1000)

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7,vi-VN;q=0.6,vi;q=0.5',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json; charset=UTF-8',
        'Origin': 'https://www.momoshop.com.tw',
        'Referer': 'https://www.momoshop.com.tw/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    json_data = {
        'host': 'momoshop',
        'flag': 'searchEngine',
        'data': {
            'specialGoodsType': '',
            'isBrandSeriesPage': False,
            'authorNo': '',
            'searchValue': 'iphone14',
            'cateCode': '',
            'cateLevel': '-1',
            'cp': 'N',
            'NAM': 'N',
            'first': 'N',
            'freeze': 'N',
            'superstore': 'N',
            'tvshop': 'N',
            'china': 'N',
            'tomorrow': 'N',
            'stockYN': 'N',
            'prefere': 'N',
            'threeHours': 'N',
            'video': 'N',
            'cycle': 'N',
            'cod': 'N',
            'superstorePay': 'N',
            'showType': 'chessboardType',
            'curPage': f'{page_num}',
            'priceS': '0',
            'priceE': '9999999',
            'searchType': '1',
            'reduceKeyword': '',
            'brandName': [
                'Apple 蘋果',
            ],
            'brandCode': [
                '20160808155618011',
            ],
            'isFuzzy': '0',
            'rtnCateDatainfo': {
                'cateCode': '',
                'cateLv': '-1',
                'keyword': 'iphone14',
                'curPage': f'{page_num}',
                'historyDoPush': False,
                'timestamp': timestamp,
            },
            'flag': 2018,
        },
    }

    response = requests.post(
        'https://apisearch.momoshop.com.tw/momoSearchCloud/moec/textSearch', headers=headers, json=json_data)

    data = response.json()
    return {
        'min_page': data['minPage'],
        'max_page': data['maxPage'],
        'cur_page': data['curPage'],
        'total_cnt': data['totalCnt'],
        'cur_page_goods_cnt': data['curPageGoodsCnt'],
        'goods_info_list': data['rtnSearchData']['goodsInfoList'],
    }


def write_json(data: Union[list, dict], filename: str):
    with open(filename, 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_json(filename: str) -> Union[list, dict]:
    with open(filename, 'r', encoding='utf8') as f:
        data = json.load(f)
    return data


def crawl_to_json(today: str):
    iphone_items = []

    p1_data = get_iphone14_page_n(1)
    iphone_items.extend(p1_data['goods_info_list'])
    cur_page = p1_data['cur_page']
    max_page = p1_data['max_page']

    print(f'max_page: {max_page}')
    print(f'page {cur_page} crawled')
    while cur_page < max_page:
        cur_page += 1
        pn_data = get_iphone14_page_n(cur_page)
        iphone_items.extend(pn_data['goods_info_list'])
        print(f'page {cur_page} crawled')

    write_json(iphone_items, f'{today}_iphones.json')


def clean_price(price: str) -> int:
    price = price.replace(',', '')
    price = price.replace('$', '')
    match = re.search(r'\d+', price)
    if match:
        return int(match.group())


def store_json_to_db(today: str):
    iphone_items = load_json(f'{today}_iphones.json')

    for item in iphone_items:
        product = {
            'id': item['goodsCode'],
            'name': item['goodsName'],
            'price': clean_price(item['goodsPrice']),
        }
        product = ProductSchema(**product)

        response = requests.post(
            'http://localhost:80/products', json=product.dict())
        if response.status_code == 400:
            response = requests.patch(
                f'http://localhost:80/products/{product.id}', json=product.dict())
            assert response.status_code == 200, response.json()

        else:
            print('create a product:', response.json()['id'])


def main():
    today = datetime.now(tz=ZoneInfo('Asia/Taipei')).strftime('%Y%m%d')

    crawl_to_json(today)
    store_json_to_db(today)


if __name__ == '__main__':
    main()

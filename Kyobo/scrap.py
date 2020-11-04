import pandas as pd
from bs4 import BeautifulSoup
import requests

class KyoboScraper():
    def __init__(self, **kwargs):
        self.key = kwargs['key']
        self.pages = int(kwargs['pages'])+1
        self.name = kwargs['name']

    def scrap_links(self):
        key = self.key
        pages = self.pages
        links = []
        for i in range(1, pages):
            res = requests.get(key.format(i))
            html = res.text
            soup = BeautifulSoup(html, 'lxml')
            temp_links = soup.select('tbody#search_list td.detail > div.title > a')
            links.append([a['href'] for a in temp_links])
            print('진행률 = {} / {}'.format(i, pages-1))
        links = sum(links, [])
        print('링크 수집이 완료되었습니다.')
        return links

    def scrap_books(self,links):
        links = links
        name = self.name
        titles = []
        dates = []
        prices = []
        count = 0

        print('도서 수집을 시작합니다.')
        for link in links:
            count += 1
            res = requests.get(link)
            html = res.text
            soup = BeautifulSoup(html, 'lxml')
            titles.append(soup.select_one('div.box_detail_point h1.title > strong').text.strip())
            temp = soup.select_one('div.author span.date').text
            dates.append(temp[:temp.find('출간')].strip())
            prices.append(soup.select_one('ul.list_detail_price span.sell_price').text.strip()[:-1])

            print("도서명 : {} | 진행률 : {}/{}".format(titles[-1], count, len(links)))
        print('도서 수집이 완료되었습니다.')

        df = pd.DataFrame({'도서명': titles, '판매시작일': dates, '가격': prices})
        df.to_csv('./data/{}.csv'.format(name))
        print('도서 리스트를 csv파일로 저장하였습니다. 저장 경로는 현재 실행 위치입니다.')

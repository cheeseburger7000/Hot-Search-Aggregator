import requests
from bs4 import BeautifulSoup

class WebNews:
    def __init__(self, rank, url, title, heat, news_type):
        self.rank = rank
        self.url = url
        self.title = title
        self.heat = heat
        self.news_type = news_type

web_hot_search_url = 'https://s.weibo.com/top/summary'
web_hot_search_root = 'https://s.weibo.com'

res = requests.get(web_hot_search_url)
status = res.status_code
if res.status_code == 200:
    soup = BeautifulSoup(res.content, 'html.parser')
    items = soup.find('div', { 'id': 'pl_top_realtimehot' }).find('table').find('tbody').find_all('tr')
    for item in items:
        # rank
        rank_list = item.find_all('td', class_='td-01 ranktop', limit=1)
        if rank_list:
            rank = rank_list[0].text
        else:
            rank = 'top'
        
        # url
        url_title_heat = item.find_all('td', class_='td-02', limit=1)[0]
        url_title = url_title_heat.find('a', href=True)
        relative_path = url_title['href']
        url = web_hot_search_root + relative_path
        # title
        title = url_title.text
        # heat 热度
        heat = url_title_heat.find('span')
        # type
        news_type = item.find_all('td', class_='td-03', limit=1)[0].text
        # news = WebNews(rank, url, title, heat, news_type)
        news = {}
        news['rank'] = rank
        news['url'] = url
        news['title'] = title
        news['news_type'] = news_type

        print(news)

# TODO error
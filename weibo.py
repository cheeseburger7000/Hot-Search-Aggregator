import requests
from bs4 import BeautifulSoup
import re
# import json
# from datetime import date

WEIBO_TOP_URL = 'https://s.weibo.com/top/summary'
WEIBO_ROOT_URL = 'https://s.weibo.com'


def extract_rank(node):
    """
    提取热搜排名
    :param node: 热搜 HTML 节点
    :return: 热搜排名
    """
    rank_list = node.find_all('td', class_='td-01 ranktop', limit=1)
    if rank_list:
        rank = rank_list[0].text
    else:
        rank = 'TOP'
    return rank


def extract_url(node):
    """
    提取热搜 URL 路径
    :param node: 热搜 HTML 节点
    :return: 热搜 URL 路径
    """
    url_title_heat = node.find_all('td', class_='td-02', limit=1)[0]
    url_title = url_title_heat.find('a', href=True)
    relative_path = url_title['href']
    return WEIBO_ROOT_URL + relative_path


def extract_title(node):
    """
    提取热搜标题
    :param node: 热搜 HTML 节点
    :return: 热搜标题
    """
    url_title_heat = node.find_all('td', class_='td-02', limit=1)[0]
    url_title = url_title_heat.find('a', href=True)
    return url_title.text


def extract_heat(node):
    """
    提取热搜热度
    :param node: 热搜 HTML 节点
    :return: 热搜热度
    """
    url_title_heat = node.find_all('td', class_='td-02', limit=1)[0]
    heat_tag = url_title_heat.find('span')
    only_number = r'\d+'
    r = re.findall(only_number, str(heat_tag))
    if r:
        heat = int(r[0])
    else:
        heat = None
    return heat


def extract_news_type(node):
    """
    提取热搜类型
    :param node: 热搜 HTML 节点
    :return: 热搜类型
    """
    return node.find_all('td', class_='td-03', limit=1)[0].text


res = requests.get(WEIBO_TOP_URL)
status = res.status_code
if res.status_code == 200:
    soup = BeautifulSoup(res.content, 'html.parser')
    items = soup.find('div', {'id': 'pl_top_realtimehot'}).find('table').find('tbody').find_all('tr')
    result = []
    for item in items:
        rank = extract_rank(item)
        url = extract_url(item)
        title = extract_title(item)
        heat = extract_heat(item)
        news_type = extract_news_type(item)

        news = {'rank': rank, 'url': url, 'title': title}
        if news_type:
            news['news_type'] = news_type
        if heat is not None:
            news['heat'] = heat
        result.append(news)

    # today = date.today()
    # file_path = f'examples/weibo{str(today)}.json'
    # with open(file_path, 'w') as f:
    #     json.dump(result, f, ensure_ascii=False, indent=4)
    # print('DONE!')
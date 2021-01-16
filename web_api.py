from flask import Flask, make_response
import os

from weibo import do as weibo_do
from baidu import do as baidu_do

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/')
def home():
    weibo_items = weibo_do()
    baidu_items = baidu_do()
    result = {'微博热搜': weibo_items, '百度热榜': baidu_items}
    # todo UI
    response = make_response(result)
    response.status = '200'
    response.headers['Content-Type'] = 'application/json;charset=utf-8'
    return response


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)

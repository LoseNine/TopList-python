import requests
from lxml import etree

headers={
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}

url='https://www.zhihu.com/hot'
html=requests.get(url,headers=headers)
soup=etree.HTML(html.text)
items=soup.xpath('//div[@class="HotList-list"]/section')
for item in items:
    title=item.xpath('div[2]/a/h2/text()')[0]
    content=item.xpath('div[2]/a/p/text()')
    url=item.xpath('div[2]/a/@href')[0]
    print(title,url,content)
from lxml import etree
from urllib import parse
from models import Block,Hot
import aiohttp
import asyncio
from concurrent.futures import ThreadPoolExecutor

threadpool=ThreadPoolExecutor(100)

class CrawlData:
    def __init__(self):
        self.urls={
            'V3EX':'https://www.v2ex.com/?tab=hot',
            'Github':'https://github.com/trending',
            'WeiBo':'https://s.weibo.com/top/summary',
            'ZhiHu':'https://www.zhihu.com/hot',
        }
        self.headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        }

    async def getConn(self,name):
        url=self.urls.get(name)
        async with aiohttp.ClientSession(headers=self.headers)as session:
            async with session.get(url)as resp:
                if resp.status==200:
                    soup=etree.HTML(await resp.text())
                    return soup
                else:
                    print('获取{}失败'.format(name))
                    return None


    async def GetZhiHu(self):
        url = 'https://www.zhihu.com/hot'
        self.headers['cookie']='_zap=d3b85524-608a-40a0-a0c8-6cb65d433f06; d_c0="ACAhXCO-BRCPTl_RLKNCOS6yneaLpF29q4E=|1568043294"; tgw_l7_route=f2979fdd289e2265b2f12e4f4a478330; _xsrf=cbc8c703-c14e-4a2f-8e4d-3d80c4da82da; capsion_ticket="2|1:0|10:1568095339|14:capsion_ticket|44:Zjg4ZmRjMmY2ZTJjNDVkNTgwMWNiNjA1NjU5NTYzMzA=|506899d0030a455c56324b2bdf2592270dce960f4187dd6111662ee61824fb12"; l_n_c=1; r_cap_id="MmM4NjBkNTI0YTc4NGFmNGFiM2FjYzUwY2RkMmE0ZmQ=|1568095343|54d1cfb6dc5004e521366794171e1b01c584ef6b"; cap_id="MTI2MTIwNThhNWRlNGI1YzhjMzU5ZDEzZTQxZTJiMzg=|1568095343|2d87297fbb65212e7c20c6de9b35e64bce784945"; l_cap_id="ODI1N2Y0YjVhMDViNDI1Mjk2ZTkyNTY1M2RlMGYxZTQ=|1568095343|82490ce4fb492327ee04ba45315ec8906b136728"; n_c=1; z_c0=Mi4xQ09MUkNRQUFBQUFBSUNGY0k3NEZFQmNBQUFCaEFsVk5lb3BrWGdENlJUT1Vwc3BIdkgzSVhXN0pGUExPVlRvZU1R|1568095354|fc1d394d3725d0934fc9fd6b606932e1bb7ad659; tshl=; tst=h; unlock_ticket="AJBihgA5qw0XAAAAYQJVTYVDd10T-ZK-VwMEje_V-X8D4kfV2fn6TA=="'
        async with aiohttp.ClientSession(headers=self.headers)as session:
            async with session.get(url)as resp:
                if resp.status==200:
                    soup=etree.HTML(await resp.text())
                else:
                    print('获取{}失败'.format(url))
                    return None
        items = soup.xpath('//div[@class="HotList-list"]/section')
        for item in items:
            title = item.xpath('div[2]/a/h2/text()')[0]
            content = item.xpath('div[2]/a/p/text()')
            url = item.xpath('div[2]/a/@href')[0]
            if content:
                content=content[0].strip()
            else:
                content=''
            print(title, url, content)
            threadpool.submit(Hot.addHot, title=str(title), url=str(url), block='ZhiHu', content=content)
            #await Hot.addHot(title=str(title), url=str(url), block='ZhiHu', content=content)

    async def GetWeiBo(self):
        soup = await self.getConn('WeiBo')
        items = soup.xpath('//div[@class="data"]/table/tbody/tr')
        for item in items:
            title = item.xpath('td[2]/a/text()')[0]
            url = parse.urljoin('https://s.weibo.com',item.xpath('td[2]/a/@href')[0])
            print(title, url)
            threadpool.submit(Hot.addHot, title=str(title), url=str(url), block='WeiBo', content='')
            #await Hot.addHot(title=str(title), url=str(url), block='WeiBo', content='')

    async def GetGithub(self):
        soup=await self.getConn('Github')
        items=soup.xpath('//article[@class="Box-row"]')
        for item in items:
            title=item.xpath('h1/a/span[2]/text()')[0].strip().replace('/','')
            url=item.xpath('h1/a/@href')[0].strip()
            try:
                content=item.xpath('p[contains(@class,"col-9")]/text()')[0].strip()
            except:
                content=''
            if title and url:
                url=parse.urljoin('https://github.com/',url)
                print(title, url,content)
                threadpool.submit(Hot.addHot,title=str(title), url=str(url), block='Github', content=content)
                #await Hot.addHot(title=str(title), url=str(url), block='Github', content=content)

    async def GetV3EX(self):
        soup = await self.getConn('V3EX')
        if soup:
            items=soup.xpath('//div[@id="Main"]/div[@class="box"]/div[contains(@class,"cell")]')[1:]
            for item in items:
                title=item.xpath('table//td[3]/span/a/text()')
                url=item.xpath('table//td[3]/span/a/@href')
                if title and url:
                    url = parse.urljoin('https://www.v2ex.com/', url[1])
                    print(title[1],url)
                    threadpool.submit(Hot.addHot, title=str(title[0]), url=str(url), block='V3EX', content='')
                    #Hot.addHot(title=str(title[0]),url=str(url),block='V3EX',content='')
        else:
            print('GetV3EX Error Done')


def ExecGetData(spider,value):
    dataType=getattr(spider,"Get"+value)
    return dataType

def main():
    allData=[
        'Github',
         'WeiBo',
         'V3EX',
         'ZhiHu'
    ]
    loop = asyncio.get_event_loop()
    print("开始抓取{}种数据类型".format(len(allData)))
    spider = CrawlData()
    tasks=[]
    for _,value in enumerate(allData):
        print("开始抓取"+value)
        Block.addBlock(value)
        func=ExecGetData(spider,value)
        tasks.append(func())
    loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()

if __name__ == '__main__':
    main()
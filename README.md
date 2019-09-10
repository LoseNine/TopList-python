# pyTopList
今日热榜项目TopList的Python实现，灵感来源：
今日热榜tophubs/TopList，一个获取各大热门网站热门头条的聚合网站，使用Go语言编写，多协程异步快速抓取信息，预览:https://www.printf520.com/hot.html

**用Python复现Go语言的TopList，使用python语言编写的异步爬虫**

![1.png](https://github.com/LoseNine/pyTopList/blob/master/static/imgs/1.PNG)

### 目录说明

```
TopList/
├── App
|   |——__init__.py  项目初始化配置app
│   ├── GetHot.py   爬取热榜的爬虫程序
│   └── models.py   SQLALchemy数据库模型
├── Config
│   └── config.py   Flask项目的配置文件
├── static 静态文件
│   ├── css   
|   ├── fonts
|   ├── imgs 
│   └── js
├── templates 前端模板文件
│   └── index.html
├── test 写测试的
│   └── get.py
├── Server.py 项目的启动入口
└── README.md
```

### 安装教程
 
1. 创建MYSQL数据库，如 `toplist`作为数据库名

3. 编辑文件 `Config/cofig.py`
```
  SQLALCHEMY_DATABASE_URI='mysql://root:root@localhost/toplist' 连接你的数据库
```

4. 运行Server.py后，运行爬虫程序`App/GetHot.py`爬取各大热榜

5. 浏览测试

   - 打开`http://127.0.0.1:8080/` 

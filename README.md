# pyTopList
今日热榜项目TopList的Python实现，来源：（今日热榜tophubs/TopList，一个获取各大热门网站热门头条的聚合网站，使用Go语言编写，多协程异步快速抓取信息，预览:https://www.printf520.com/hot.html）

**用Python复现Go语言的TopList，使用python语言编写的异步爬虫**

![1.png](https://github.com/LoseNine/pyTopList/blob/master/templates/imgs/1.PNG)
### 安装教程
 
1. 创建MYSQL数据库，如 `toplist`

3. 编辑文件 `Config/cofig.py`
```
  SQLALCHEMY_DATABASE_URI='mysql://root:root@localhost/toplist'
```

4. 运行Server.py后，运行爬虫程序`App/GetHot.py`

5. 测试

   - 打开`http://127.0.0.1:8080/` 

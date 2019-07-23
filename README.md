### 使用Scrapy爬取B站番剧基本信息

使用scrapy框架爬取B站的三千部左右的番剧的基本信息并存入MySQL数据库中，关键地方有注释，可以作为scrapy学习过程中的参考

如果想要自行爬取请修改`settings.py`中的本地数据库连接信息，并创建一张表

```sql
-- table DDL
CREATE TABLE `bilibili_index` (
  `media_id` decimal(10,0) NOT NULL,
  `name` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `play_href` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `cover_url` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `pub_time` decimal(10,0) DEFAULT NULL,
  `watch_number` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `followed_number` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `bilibili_score` decimal(2,1) DEFAULT NULL,
  `detailed_url` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `desc` varchar(900) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `tags` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `cv` varchar(200) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `staff` varchar(200) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`media_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
```

然后使用`scrapy crawl index`命令即可

附：三千余部番剧基本信息数据库 [下载地址](https://www.dropbox.com/s/wg09t0qx7ypt70k/bilibili_index.sql?dl=0) (DropBox链接，需科学上网)



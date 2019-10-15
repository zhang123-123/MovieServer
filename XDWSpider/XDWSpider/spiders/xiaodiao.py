# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urljoin
from ..items import MovieItem


class XiaodiaoSpider(scrapy.Spider):
    name = 'xiaodiao'
    allowed_domains = ['dytt8.net']
    start_urls = ['https://www.dytt8.net/']
    custom_settings = {
        "ROBOTSTXT_OBEY": False,
        "CONCURRENT_REQUESTS": 4,
        "DOWNLOAD_DELAY": 1,
        "COOKIES_ENABLED": False,
        "ITEM_PIPELINES": {
            'XDWSpider.pipelines.ImagePipeline': 300,
        },
        "DOWNLOADER_MIDDLEWARES": {
            'XDWSpider.rand_agent.UserAgentMiddleware': 543,
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None
        },
        "IMAGES_STORE": "../static",
        # 图片下载地址
        "IMAGES_URLS_FIELD": "movie_img",
    }

    def parse(self, response):
        yield scrapy.Request(
            url=response.url,
            callback=self.parse_cates,
            dont_filter=True,
            meta={}
        )

    def parse_cates(self, response):
        cates = response.xpath("//div[@class='contain']/ul/li/a")[3:4]
        for cate in cates:
            cate_name = cate.xpath("text()").get()
            cate_href = cate.xpath("@href").get()
            # cate_href = urljoin(response.url, cate_href)
            print(cate_name, cate_href)
            yield scrapy.Request(
                url=cate_href,
                callback=self.parse_all_page,
                dont_filter=True,
                meta={
                    "cate_name": cate_name
                }
            )
            # break

    def parse_all_page(self, response):
        meta = response.meta
        all_pages = response.xpath("//select[@name='sldd']/option")
        for all_page in all_pages:
            page_url = all_page.xpath("@value").get()
            page_url = urljoin(response.url, page_url)

            print(page_url)
            yield scrapy.Request(
                url=page_url,
                callback=self.parse_one_page,
                dont_filter=True,
                meta={
                    "cate_name": meta["cate_name"]
                }
            )
            # break

    def parse_one_page(self, response):
        meta = response.meta
        # movie_infos = response.xpath("//div[@class='co_content8']/ul/td/table/b/a")
        movie_infos = response.xpath("//b/a[@class='ulink']")
        # print(len(movie_infos))
        for movie_info in movie_infos:
            movie_name = movie_info.xpath("text()").get()
            movie_href = movie_info.xpath("@href").get()
            if "index.html" in movie_href:
                continue
            # print(movie_href)
            # if ".html" in movie_href:
            movie_href = urljoin(response.url, movie_href)
            # print(movie_name, movie_href)

            yield scrapy.Request(
                url=movie_href,
                callback=self.parse_detail,
                dont_filter=True,
                meta={
                    "cate_name": meta["cate_name"],
                    "movie_name": movie_name
                }
            )
            # break

    def parse_detail(self, response):
        meta = response.meta
        movie_infos = response.xpath("//div[@id='Zoom']/td//text()").getall()
        print(movie_infos)
        movie_lists = []
        for movie_info in movie_infos:
            if movie_info:
                movie_info = movie_info.strip().replace("\u3000", "").replace("\xa0", "")
                if movie_info:
                    movie_lists.append(movie_info)
        print(movie_lists)
        """
        电影名   译名(trans_name)    片名(movie_title)   年代(movie_age)  产地(movie_price)
        类别(movie_cate)      语言(movie_language)  字幕(movie_subtitle)  上映日期(movie_release_time)
        IMDb评分(movie_imdb)  豆瓣评分(movie_douban)    文件格式(movie_file_format)    视频尺寸(movie_video_size)
        文件大小(movie_file_size)    片长(movie_length)  导演(movie_director)  编剧(movie_screenwriter)
        主演(movie_starring)  标签(movie_label)  简介(movie_introduction)
        """
        trans_name = ""
        movie_title = ""
        movie_age = ""
        movie_place = ""
        movie_cate = ""
        movie_language = ""
        movie_subtitle = ""
        movie_release_time = ""
        movie_imdb = ""
        movie_douban = ""
        movie_file_format = ""
        movie_video_size = ""
        movie_file_size = ""
        movie_length = ""
        movie_director = ""
        movie_screenwriter = ""
        movie_starring = ""
        movie_label = ""
        movie_introduction = ""
        movies = "".join(movie_lists)
        movie_strs = movies.split("◎")
        print(movie_strs)
        # movie_ =
        for movie_str in movie_strs:
            movie_str = "◎" + movie_str
            if "◎译名" in movie_str:
                trans_name = movie_str.split("名")[1]
            if "◎片名" in movie_str:
                movie_title = movie_str.split("名")[1]
            if "◎年代" in movie_str:
                movie_age = movie_str.split("代")[1]
            if "◎产地" in movie_str:
                movie_place = movie_str.split("地")[1]
            if "◎类别" in movie_str:
                movie_cate = movie_str.split("别")[1]
            if "◎语言" in movie_str:
                movie_language = movie_str.split("言")[1]
            if "◎字幕" in movie_str:
                movie_subtitle = movie_str.split("幕")[1]
            if "◎上映日期" in movie_str:
                movie_release_time = movie_str.split("期")[1]
            if "◎I" in movie_str or "◎i" in movie_str:
                movie_imdb = movie_str.split("分")[1]
            if "◎豆瓣评分" in movie_str:
                movie_douban = movie_str.split("分")[1]
            if "◎文件格式" in movie_str:
                movie_file_format = movie_str.split("式")[1]
            if "◎视频尺寸" in movie_str:
                movie_video_size = movie_str.split("寸")[1]
            if "◎文件大小" in movie_str:
                movie_file_size = movie_str.split("小")[1]
            if "◎片长" in movie_str:
                movie_length = movie_str.split("长")[1]
            if "◎导演" in movie_str:
                movie_director = movie_str.split("演")[1]
            if "◎编剧" in movie_str:
                movie_screenwriter = movie_str.split("剧")[1]
            if "◎主演" in movie_str:
                movie_starring = movie_str.split("演")[1]
            if "◎标签" in movie_str:
                movie_label = movie_str.split("签")[1]
            if "◎简介" in movie_str:
                movie_introduction = movie_str.split("介")[1]

        movie_img = response.xpath("//img[contains(@src, '.jpg')]/@src").get()
        movie_down_url = response.xpath("//a[contains(text(), 'ftp://')]/@href").get()
        cate_name = meta["cate_name"]
        movie_name = meta["movie_name"]
        print(cate_name, movie_name, movie_img, movie_down_url, trans_name, movie_title, movie_age, movie_place, movie_cate, movie_language, movie_subtitle, movie_release_time,
              movie_imdb, movie_douban, movie_file_format, movie_video_size, movie_file_size, movie_length,
              movie_director, movie_screenwriter, movie_starring, movie_label, movie_introduction)
        print(response.url)
        if not movie_img:
            movie_img = "http://aaa.jpg"
        item = MovieItem()
        item["cate_name"] = cate_name
        item["movie_name"] = movie_name
        item["movie_down_url"] = movie_down_url
        item["movie_img"] = [movie_img]
        item["trans_name"] = trans_name
        item["movie_title"] = movie_title
        item["movie_age"] = movie_age
        item["movie_place"] = movie_place
        item["movie_cate"] = movie_cate
        item["movie_language"] = movie_language
        item["movie_subtitle"] = movie_subtitle
        item["movie_release_time"] = movie_release_time
        item["movie_imdb"] = movie_imdb
        item["movie_douban"] = movie_douban
        item["movie_file_format"] = movie_file_format
        item["movie_video_size"] = movie_video_size
        item["movie_file_size"] = movie_file_size
        item["movie_length"] = movie_length
        item["movie_director"] = movie_director
        item["movie_screenwriter"] = movie_screenwriter
        item["movie_starring"] = movie_starring
        item["movie_label"] = movie_label
        item["movie_introduction"] = movie_introduction

        # item.save()
        yield item


    def parse_down_url(self, response):
        meta = response.meta
        img = response.xpath("//img[contains(@src, '.jpg')]/@src").get()
        # print(img)
        movie_down_url = response.xpath("//a[contains(text(), 'ftp://')]/@href").get()
        # if not movie_down_url:
        #     movie_down_url = response.xpath("")
        # print(img, movie_down_url)
        cate_name = meta["cate_name"]
        movie_name = meta["movie_name"]
        print(cate_name, movie_name, img, movie_down_url, response.url)
        if not img:
            img = "http://aaa.jpg"
        item = MovieItem()
        item["cate_name"] = cate_name
        item["movie_name"] = movie_name
        item["movie_down_url"] = movie_down_url

        item["img"] = [img]
        # item.save()
        yield item

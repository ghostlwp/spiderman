# -*- coding: utf-8 -*-
import hashlib
import json
import time
import pymongo
import scrapy
from urllib.parse import urlencode
from toutiao.settings import mongo_host,mongo_port,mongo_db_name,mongo_db_collection
from toutiao.items import ToutiaoItem
from toutiao.keywords import  KEYWORDS

offset = 0
cookies={ 'CNZZDATA1259612802':'1970965750-1562910301-%7C1564992139',
          'RT':'\"z=1&dm=toutiao.com&si=y8h4cgrz4ya&ss=jyxusugb&sl=1&tt=9kj&nu=5f2ae476426021582acbbcbe42cce319&cl=265pa&ld=268f7&r=a3bc1f2a4a531650a600dc538df429c1&ul=268f9&hd=268je\"',
          'UM_distinctid':'16be502c4ac6e9-04d424c9cac24c-37607e02-1fa400-16be502c4ad7f7',
          'WEATHER_CITY':'%E5%8C%97%E4%BA%AC',
          '__tasessionId':'71mn2yz2b1564992178552',
          '__tea_sdk__ssid':'b02a4492-cdab-4095-99ec-f2c7bd873ef4',
          '__tea_sdk__user_unique_id':'2941921661823917',
          '_ga':'GA1.2.1684737303.1561100694',
          'aefa4e5d2593305f_gr_cs1':'2941921661823917',
           'aefa4e5d2593305f_gr_last_sent_cs1':'2941921661823917',
           'ccid':'54dc81e8f9271dbbbb4abca57035e0ba',
           'csrftoken':'d851cd3d621b582e40c65b1eac86ac14',
           'gr_user_id':'8ff8998e-3324-495b-9784-e22d679462b5',
           'grwng_uid':'daf2e91e-a457-4bbe-a4de-a47ec93f797b',
           's_v_web_id':'1fcffa7a6292096adfaa6dfe26f57092',
           'sid_guard':'\"07cb51ec15626e3d1cff4f0a04ff569f|1562066077|1626782|Sun\054 21-Jul-2019 07:07:39 GMT\"',
           'sso_uid_tt':'38f0d150b6bfa976cfcc44b4bf8282da',
           'toutiao_sso_user':'b505533941ec421cc34370254d3fc51a',
           'tt_webid':'6704876972995053064',
           'tt_webid':'6704876972995053064',
           'uuid':'\"w:e3734597b1fd4cb196d64ef4b4a71728\"'}
client =pymongo.MongoClient(host=mongo_host,port=mongo_port)
db = client[mongo_db_name]
collection = db[mongo_db_collection]


class toutiaoSpiderSpider(scrapy.Spider):
    name = 'toutiao_spider'
    allowed_domains = ['www.toutiao.com']

#转换
    def start_requests(self):
        for keyword in KEYWORDS:
            offset = 0
            while offset < 50:
                timestamp = int(round(time.time() * 1000))
                data={
                    'keyword': keyword,
                    'offset':offset,
                    'format':'json',
                    'autoload':'true',
                    'count':20,
                    'en_qc':1,
                    'cur_tab':1,
                    'from':'gallery',
                    'timestamp':timestamp
                }
                print(urlencode(data))
                url="https://www.toutiao.com/api/search/content/?"+urlencode(data)
                offset += 1
        # yield scrapy.Request(url, meta={'cookiejar': cookie_jar}, callback=self.parse)
                yield scrapy.Request(url, cookies=cookies, callback=self.parse)

    def parse(self, response):
        js = json.loads(response.body.decode('utf-8'))
        data = js['data']
        # cookie = response.headers.getlist('Set-Cookie')[0].split(';')[0]
        # print(cookie)
        for d in data:
            image_list=d.get('image_list')
            if image_list:
                for item in image_list:
                    toutiao_item=ToutiaoItem()
                    url=item.get('url')
                    new_image_url = url.replace('list', 'large').replace('/190x124','')
                    pic_id = hashlib.md5(new_image_url.encode("utf8")).hexdigest();
                    result = collection.find_one({"pic_id": pic_id})
                    if(result):
                        print("continue")
                        continue
                    else:
                        toutiao_item["pic_id"] = pic_id
                        toutiao_item["pic_link"] = new_image_url
                        toutiao_item["pic_desc"] = "jj"
                        yield toutiao_item


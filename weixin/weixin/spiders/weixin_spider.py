# -*- coding: utf-8 -*-
import time
import pymongo
import scrapy
import hashlib
import random
from weixin.mongoop import getCollectionCount,pageQuery
from urllib.parse import urlencode

from weixin.items import WeixinItem
from scrapy.http.cookies import CookieJar
from weixin.settings import mongo_host,mongo_port,mongo_db_name,mongo_db_collection

from weixin.keywords import KEYWORDS

cookies={ 'CXID':'5D7678CFCDB3A32B6F9173A9EA7E3F4B',
          'SUID':'7B3DC9713865860A5C05E0580006242D',
          'SUV':'006DDB9771C93D7B5C9F64BAF0F03933',
          'IPLOC':'CN6101',
          'LSTMV':'417%2C419',
          'LCLKINT':'2377',
          'sw_uuid':'9978024583',
          'ssuid':'2648337505',
           'usid':'YwwesJLxkUlV8Zip',
           'wuid':'AAEY61cqKAAAAAqKJTAiFgEAAAA=',
           'front_screen_resolution':'1920*1080',
           'FREQUENCY':'1561014545127_2',
           'weixinIndexVisited':'1',
           'JSESSIONID':'aaacRshCjXHRnf4FTGiRw',
            'PHPSESSID':'3sqvoeq2husrsoa49it34c2087',
            'ABTEST':'0|1564386930|v1',
           'ad':'1yllllllll2teEdJlllllV1MHBwllllltt6dWZllllGlllll4qxlw@@@@@@@@@@@',
           'ppinf':'5|1564643887|1565853487|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToyNzolRTUlODglOTglRTklQUQlOEYlRTklQjklOEZ8Y3J0OjEwOjE1NjQ2NDM4ODd8cmVmbmljazoyNzolRTUlODglOTglRTklQUQlOEYlRTklQjklOEZ8dXNlcmlkOjQ0Om85dDJsdUh3bWhaS19zdThvelVtbTJlU1c0Q01Ad2VpeGluLnNvaHUuY29tfA; pprdig=GaWo_Ankbp2nTuB6Ru1leLpIDlPFL_k6lkmOg53TKJp4hM2KywIJmr_pmlZfujMTn7ozXsxhP1TW4GND6Ei7_W4GyxvRufzN77Wg2mbLce-ocjsiA9htdh9-ycb6w7od221ZJ8z_2vX4kePhc9E3a0GVVEn1NvnUMRtVayRO-j8',
           'sgid':'18-42306661-AV1Ckia8Mu2iaSVed2WRWBJJc',
           'SNUID':'7137C378090F85031AFF42FF0A02E778',
            'ppmdig':'15646474920000009827f6ffe8bd4cabecfb45fa43e682ef',
           'sct':'102'}
client =pymongo.MongoClient(host=mongo_host,port=mongo_port)
db = client[mongo_db_name]
collection = db[mongo_db_collection]

class WeixinSpiderSpider(scrapy.Spider):
    name = 'weixin_spider'
    allowed_domains = ['weixin.sogou.com']
    # start_urls = ['https://weixin.sogou.com/weixin?type=2&s_from=input&query=%E8%BD%A6%E8%AF%84&ie=utf8&_sug_=n&_sug_type_=&w=01019900&sut=6073&sst0=1563764542178&lkt=1%2C1563764542076%2C1563764542076']

#转换
    def start_requests(self):
        cookie_jar = CookieJar()
        for keyword in KEYWORDS:
            timestamp = int(round(time.time() * 1000))
            data={
                'query': keyword,
                '_sug_type_': None,
                'sut': '0',
                'lkt': '0,0,0',
                's_from': 'input',
                '_sug_': 'n',
                'type': '2',
                'sst0': timestamp,
                'page': 1,
                'ie': 'utf8',
                'w': '01015002',
                'dr': '1'
            }
            url="https://weixin.sogou.com/weixin?"+urlencode(data)
        # yield scrapy.Request(url, meta={'cookiejar': cookie_jar}, callback=self.parse)
            yield scrapy.Request(url, cookies=cookies, callback=self.parse)
    def parse(self, response):
        artic_list=response.xpath("//div[@class='txt-box']")
        # cookie = response.headers.getlist('Set-Cookie')[0].split(';')[0]
        # print(cookie)
        for item in artic_list:
            artic_link=item.xpath(".//a/@data-share").extract_first()
            new_artic_link=artic_link.replace("http","https")
            print(new_artic_link)
            # yield scrapy.Request(new_artic_link, meta={'cookiejar': response.meta['cookiejar']}, callback=self.parse_artic)
            yield scrapy.Request(new_artic_link, cookies=cookies, callback=self.parse_artic)
        next_link=response.xpath("//div[@class='p-fy']/a[@id='sogou_next']/@href").extract_first()
        print("_________________"+next_link)
        if next_link:
            # yield scrapy.Request("https://weixin.sogou.com/weixin" + next_link, meta={'cookiejar': response.meta['cookiejar']}, callback=self.parse)
            yield scrapy.Request("https://weixin.sogou.com/weixin" + next_link, cookies=cookies, callback=self.parse)

    def parse_artic(self, response):
        # print(response.text)
        # print("---------------------")
        # print(response.xpath("//div[@id='js_content']/p/img/@data-sr  c").extract());
        for item in response.xpath("//div[@id='js_content']/p/img/@data-src").extract():
            weixin_item=WeixinItem()
            pic_id=hashlib.md5(item.encode("utf8")).hexdigest();
            result=collection.find_one({"pic_id": pic_id})
            if(result):
                print("continue")
                continue
            else:
                desc=self.getPicDesc()
                weixin_item["pic_id"] = pic_id
                weixin_item["pic_link"] = item
                weixin_item["pic_desc"] = desc
                yield weixin_item

    def getPicDesc(self):

        # 感叹词+主语+宾语+行为+地点+时间+国家
        desc=self.getWord("interjection")+" "+self.getWord("subject")+" "+self.getWord("object")+" "+self.getWord("action")+" "+self.getWord("location")+" "+self.getWord("time")+" in "+self.getWord("country")
        print(desc)
        return desc

    def getWord(self,collectionName):
        subjectCount = getCollectionCount(collectionName)
        subjectIndex = random.randint(1, subjectCount)
        print(subjectIndex)
        results = pageQuery(collectionName, None, 1, subjectIndex)
        result = results[0]
        word = result['ename']
        return word

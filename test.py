import requests
from lxml import etree
import json

class ShiciSpider:
    def __init__(self):
        self.start_url ="http://so.gushiwen.org/type.aspx"
        self.domain = "http://so.gushiwen.org"
        self.headers={"user-agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Mobile Safari/537.36"}

    def parse_url(self, url):  # 发送请求，获取响应
        print("请求url:%s" %url)
        response = requests.get(url, headers=self.headers)
        return response.content.decode()

    def get_content_list(self,html_str):#提取数据
        html = etree.HTML(html_str,etree.HTMLParser())
        div_list = html.xpath('//div[@class="left"]/div[@class="sons"]') #根据div分组
        content_list = []
        next_url = None
        for row in div_list:
            item = {}
            item["title"] = row.xpath('div[@class="cont"]/p/a/b/text()')[0] if row.xpath('div[@class="cont"]/p/a/b/text()') else None
            item["dynasty"] = row.xpath('div[@class="cont"]/p[@class="source"]//text()')[0] if row.xpath('div[@class="cont"]/p[@class="source"]//text()') else ''
            item["author"] = row.xpath('div[@class="cont"]/p[@class="source"]//text()')[-1] if row.xpath('div[@class="cont"]/p[@class="source"]//text()') else ''
            item["content"] = ''.join(row.xpath('div[@class="cont"]/div[@class="contson"]//text()')).replace('  ', '').replace('\n', '').replace('\u3000','') if row.xpath('div[@class="cont"]/div[@class="contson"]//text()') else ''
            item["tag"] = ','.join(row.xpath('div[@class="tag"]/a/text()')) if row.xpath('div[@class="tag"]/a/text()') else ''
            content_list.append(item)
        if(html.xpath('//div[@class="pagesright"]/a[@class="amore"]/@href')):
            next_url = self.domain + html.xpath('//div[@class="pagesright"]/a[@class="amore"]/@href')[0]
            print(next_url)
        return content_list,next_url

    def save_content_list(self, content_list):  # 保存数据
        file_path = "诗词.txt"
        with open(file_path, "a", encoding="utf-8") as f:
            for content in content_list:
                f.write(json.dumps(content, ensure_ascii=False, indent=2))
                f.write("\n")
        print("保存成功")

    def save_url_list(self, next_url_start):  # 保存数据
        file_path = "诗词url.txt"
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(next_url_start)
            f.write("\n")

    def run(self):#实现主要逻辑
        next_url_start = self.start_url
        while next_url_start is not None:
            self.save_url_list(next_url_start)
            html_str = self.parse_url(next_url_start)
            content_list,next_url = self.get_content_list(html_str)
            next_url_start = next_url
            self.save_content_list(content_list)

if __name__ == '__main__':
    shiciSpider = ShiciSpider()
    shiciSpider.run()

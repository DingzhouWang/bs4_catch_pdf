import requests
import time
import urllib.request
from bs4 import BeautifulSoup
from itertools import count
#得到所有分类链接
def get_category_urls():
    category_urls = []
    url = 'http://mi.talkingdata.com/reports.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html')
    categorys = soup.select('div.report-left > ul >li >a')#分类标签元素

    for category in categorys:
        category_name = category['title']
        category_url = category['href']
        if category_url.split('=')[-1] != 'all':
            category_url.append(category_url)

    return category_urls
#获取所有报告地址
#获取所有分类下的报告连接
def get_report_urls(category_urls):
    all_report_urls = []

    for category_url in category_urls:
        category_report_urls = get_category_pages(category_url)
        all_report_urls.extend(category_report_urls)

    return all_report_urls
#获取一个分类下所有页码的报告连接
def get_category_pages(category_url):
    category_report_urls = []
    for page in count(1):
        start_url = category_url + '&tag=all&page=' + str(page)

        response = requests.get(start_url)
        soup = BeautifulSoup(response.text, 'html')
        books = soup.select('div.operate-book > em > a')

        if books:
            for book in books:
                report_name = book['title']
                report_url = book['href']
                category_report_urls.append(report_url)
        else:
            break

        time.sleep(2)
#下载pdf
def download_report(report_url):
    response = requests.get(report_url)
    soup = BeautifulSoup(response.text, 'html')
    download_link = soup.find('button')['data-url']
    file_name = download_link.split('/')[-1]
    urllib.request.urlretrieve('https://' + urllib.request.quote(download_link[8:]), '{}.pdf'.format(file_name))

def spider():
    category_urls = get_category_urls()
    report_urls = get_report_urls(category_urls)

    for report_url in report_urls:
        download_report(report_url)
        time.sleep(2)

if __name__ == '__main__':
    spider()
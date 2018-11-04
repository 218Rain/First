import urllib.request, re, os

def get_url(url, path):
    #获取所有要下载的图片的地址  :param url:所有要下载的图片的地址
    re_txt = r'<div class="thumb".*?<img src="(.*?.jpg)'
    urls = re.findall(re_txt, url, re.S)
    print(urls)
    down_img(urls, path)

def get_img(url, path):
    #要爬取的页面地址       :param url:要爬取的地址
    #print(path)
    user_agent = 'Chorme/4.0 (compatible; MSIE 5.5; Windows NT)'    #加的访问头信息
    req = urllib.request.Request(url, headers={'User-Agent': user_agent})  # 加的访问头信息
    page = urllib.request.urlopen(req)
    html = page.read().decode('utf-8')  #获取网页内容并转格式
    get_url(html, path)

def down_img(urls, path):
    #下载图片及保存的名字     :param urls:图片下载地址
    for i in urls:
        print(i)
        img_name = path + '\\' + i.split('/')[-1]   #获取图片的原名称
        print(img_name)
        urllib.request.urlretrieve('http:' + i, img_name)

def down_page(start, end):
    #控制从那几页下载图片     :param start开始页，:param end结束页
    for i in range(start, end + 1):
        url = 'http://www.qiushibaike.com/pic/page/{}/?s=5115845'.format(str(i))
        #print(url)
        if not os.path.exists(str(i)):
            os.mkdir(str(i))
        get_img(url, os.path.abspath(str(i)))

def main():
    down_page(1, 10)

if __name__ == '__main__':
    main()
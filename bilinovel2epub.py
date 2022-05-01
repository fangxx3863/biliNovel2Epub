# -*- coding: utf-8 -*-
import requests
import pickle
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import sys
import shutil
from pathlib import Path
from rich.console import Console
from rich.prompt import IntPrompt
from rich.prompt import Prompt
from rich.prompt import Confirm
from ebooklib import epub
import uuid
import download
from download import download
import ssl
from PIL import Image
import io
from random import randint
from multiprocessing import Pool, set_start_method
set_start_method('spawn', force=True)

console = Console()
session = requests.Session()
# 关闭SSL证书验证
ssl._create_default_https_context = ssl._create_unverified_context
# 初始化epub工具
book = epub.EpubBook()

基础URL = "https://w.linovelib.com"

 
USER_AGENTS = [
                "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
                "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
                "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
                "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
                "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
                "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
                "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
                "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
                "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
                "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
                "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
                "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
                "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
                "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
                "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
                "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
                "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
                "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
                "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
                "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
                "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
                "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
                "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
                "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
                "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
                "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
                "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
                "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
                "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
                "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
                "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
                "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
                "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
                "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
                "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
                "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
                "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
                "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
                "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
                "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
                "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
                "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
                "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
                "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
                "UCWEB7.0.2.37/28/999",
                "NOKIA5700/ UCWEB7.0.2.37/28/999",
                "Openwave/ UCWEB7.0.2.37/28/999",
                "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
                "Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25",
             ]
 
random_agent = USER_AGENTS[randint(0, len(USER_AGENTS)-1)]
HEARDERS = {
    "cookie": "_ga=GA1.2.373713668.1646927652; _gid=GA1.2.1447053390.1651231171; Hm_lpvt_d29ecd95ff28d58324c09b9dc0bee919=1651231349; Hm_lvt_d29ecd95ff28d58324c09b9dc0bee919=1649823562,1651231165; jieqiUserInfo=jieqiUserId%3D627182%2CjieqiUserUname%3Dfangxx3863%2CjieqiUserName%3Dfangxx3863%2CjieqiUserGroup%3D3%2CjieqiUserGroupName%3D%E6%99%AE%E9%80%9A%E4%BC%9A%E5%91%98%2CjieqiUserVip%3D0%2CjieqiUserHonorId%3D1%2CjieqiUserHonor%3D%E5%A4%A9%E7%84%B6%2CjieqiUserToken%3D8ea5ef793d94938673124b15cb3a7102%2CjieqiCodeLogin%3D0%2CjieqiCodePost%3D0%2CjieqiUserPassword%3D5c82b131f01843ca05e751717d74a992%2CjieqiUserLogin%3D1651231169; jieqiVisitId=article_articleviews%3D2939; jieqiVisitInfo=jieqiUserLogin%3D1651231169%2CjieqiUserId%3D627182; night=0; PHPSESSID=bsdrsrdj916v5etol006ji2odl",
    "referer": "https://w.linovelib.com/",
    "user-agent": random_agent,
}

def 标准化JSON(s:str)->dict:
    obj = eval(s, type('js', (dict,), dict(__getitem__=lambda s, n: n))())
    return obj

# 下载函数
def 下载文件(url, path='file'):
    if isinstance(url, str):
        urlFile = Path(url.split("/")[-1])
        if urlFile.exists():
            pass
        else:
            if " " in url:
                pass
            else:
                try:
                    download(url, os.getcwd() + '/' + str(path) + '/' + os.path.basename(url), replace=False, verbose=False, timeout=5)
                except:
                    return url
    if isinstance(url, list):
        errUrls = []
        for i in url:
            urlFile = Path(i.split("/")[-1])
            if urlFile.exists():
                pass
            else:
                if " " in i:
                    pass
                else:
                    try:
                        download(i, os.getcwd() + '/' + str(path) + '/' + os.path.basename(i), replace=False, verbose=False, timeout=5)
                    except:
                        errUrls.append(i)
                        return errUrls

def 下载图片集合(urls, jobs):
    pool = Pool(int(jobs))
    errUrls = pool.map(下载文件, urls)
    errUrls = sorted(list(filter(None, errUrls)))
    while errUrls:
        for i in errUrls:
            try:
                os.remove(str(i).split("src=\"")[-1][:-3].split("/")[-1] + ".part")
            except:
                continue
        errUrls = 下载文件(errUrls)

def 写到书本(title, author, content, cover_name, cover_file, imgDir, folder=None):   
    book.set_identifier(str(uuid.uuid4()))
    book.set_title(title)
    book.set_language('zh')
    book.add_author(author)
    cover_type = cover_file.split('.')[-1]
    book.set_cover(cover_name + '.' + cover_type, open(cover_file, 'rb').read())
    写入内容 = ""
    book.spine = ["nav", ]
    IDS = -1
    文件序号 = -1
    for 卷名 in content:
        console.print("卷: " + 卷名)
        卷名标题 = "<h1>" + 卷名 + "</h1>"
        写入内容 = 写入内容 + 卷名标题
        book.toc.append([epub.Section(卷名), []])
        IDS += 1
        for 章节 in content[卷名]:
            console.print("章节: " + 章节[0])
            文件序号 += 1
            单页 = epub.EpubHtml(title = 章节[0],
                       file_name = f"{文件序号}_{章节[0]}.xhtml",
                       lang = "zh")
            章节名 = "<h2>" + 章节[0] + "</h2>"
            写入内容 = 写入内容 + 章节名 + str(章节[1]).replace("<div class=\"acontent\" id=\"acontent\">", "")
            写入内容 = 写入内容.replace('png', 'jpg')
            # 添加CSS规则
            css = '<style>p{text-indent:2em; padding:0px; margin:0px;}</style>'
            写入内容 = 写入内容 + css
            单页.set_content(写入内容)
            book.add_item(单页)
            book.toc[IDS][1].append(单页)
            book.spine.append(单页)
            写入内容 = ""
    
    imgDirList = os.listdir(imgDir)
    for filename in imgDirList:
        filetype = filename.split('.')[-1]
        # 加载图片文件
        img = Image.open(imgDir + '/' + filename)  # 'image1.jpeg' should locate in current directory for this example
        b = io.BytesIO()
        img = img.convert('RGB')
        img.save(b, 'jpeg')
        data_img = b.getvalue()

        filename = filename.replace('png', 'jpg')
        img = epub.EpubItem(file_name="file/%s" % filename,
                            media_type="image/jpeg", content=data_img)
        book.add_item(img)

    if folder is None:
        folder = ''
    else:
        isExists=os.path.exists(folder) #判断路径是否存在
        if not isExists:
            # 如果不存在则创建目录
            os.makedirs(folder)
        folder = str(folder) + '/'
    
    # 最后，需要添加NCX和导航信息
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    epub.write_epub(folder + title + '.epub', book)

def 主要():
    书籍ID = str(sys.argv[1]).split("/")[-1].split(".")[0]
    if Confirm.ask("是否下载图片? 下载图片[Y] 不下载[N] "):
        下载图片 = True
    else:
        下载图片 = False
    # 获得书籍名称
    书籍首页URL = 基础URL + f"/novel/{书籍ID}.html"
    soup = BeautifulSoup(session.get(书籍首页URL,headers=HEARDERS).text, "lxml")
    书名 = soup.find("h2",{"class":"book-title"}).text
    作者 = soup.find("div",{"class":"book-rand-a"}).text[:-2]
    简介 = soup.find(id = "bookSummary").text
    封面URL = str(soup.find("img")).split("src=\"")[-1][:-3]
    console.print(简介)

    # 解析书籍目录部分,获取URL
    目录 = dict()
    目录URL = 基础URL + f"/novel/{书籍ID}/catalog"
    soup = BeautifulSoup(session.get(目录URL,headers=HEARDERS).text, "lxml")
    章节数 = soup.find("h4",{"class": "chapter-sub-title"}).find("output").text
    远程目录 = soup.find("ol",{"id":"volumes"})
    目录集合 = 远程目录.find_all("li")
    缓存 = 目录集合[0].text
    子章节 = []

    for 单个目录 in 目录集合:
        文本 = 单个目录.text
        if 单个目录["class"][0] == "chapter-bar":
            目录[缓存] = 子章节
            缓存 = 文本
            子章节 = []
        else:
            url = urljoin(基础URL,单个目录.find("a")["href"])
            子章节.append([文本,url])
    目录[缓存] = 子章节
    
    内容 = dict()
    图片URL集合 = []
    IDS = -1
    for 卷名 in 目录:
        console.print("卷: " + 卷名)
        IDS = -1
        for 章节 in 目录[卷名]:
            内容.setdefault(卷名, []).append([章节[0]])
            IDS += 1
            console.print("章节: " + 章节[0])
            缓存内容 = ""
            章节标题 = 章节[0]
            章节URL = 章节[1]

            # 处理目录中的错误链接
            if 章节[1] == "javascript:cid(0)":
                章节[1] = 下一个URL
            else:
                下一个URL = 章节[1]
                
            while True:
                soup = BeautifulSoup(session.get(下一个URL,headers=HEARDERS).text, "lxml")
                读取参数Script = soup.find("body",{"id":"aread"}).find("script")
                读取参数Script文本 = 读取参数Script.text
                readParams = 标准化JSON(读取参数Script文本[len("var ReadParams="):])
                下一个URL = 基础URL + readParams["url_next"]
                # 判断当前章节有没有下个页面
                if "_" in 下一个URL:
                    章节.append(下一个URL)
                else:
                    break
            
            for 单章URL in 章节[1:]:
                soup = BeautifulSoup(session.get(单章URL,headers=HEARDERS).text, "lxml")
                图片集合 = soup.find_all("img")
                文章内容 = str(soup.find(id="acontent"))
                for 原始 in 图片集合:
                    图片URL集合.append(str(原始).split("src=\"")[-1][:-3])
                    替换 = "file/" + str(原始).split("src=\"")[-1][:-3].split("/")[-1]
                    文章内容 = 文章内容.replace(str(原始).split("src=\"")[-1][:-3], str(替换))
                缓存内容 = 缓存内容 + 文章内容
                console.print(f"正在处理: {单章URL}")
            内容[卷名][IDS].append(缓存内容)
            
    with open('content.pickle', 'wb') as f:
        pickle.dump(内容, f)
    with open('images.pickle', 'wb') as f:
        pickle.dump(图片URL集合, f)      
    with open('info.pickle', 'wb') as f:
        pickle.dump([书名, 作者, 封面URL], f)
        
    if 下载图片:
        下载图片集合(图片URL集合, 4)
        
    下载文件(封面URL)
    写到书本(书名, 作者, 内容, "cover", "file/"+封面URL.split("/")[-1], "file")
    shutil.rmtree('file')
    os.remove("content.pickle")
    os.remove("images.pickle")
    os.remove("info.pickle")
    os._exit()
    

if __name__ == "__main__":
    contentFile = Path("content.pickle")
    imagesFile = Path("images.pickle")
    if contentFile.exists() or imagesFile.exists():
        if Confirm.ask("检测到上次失败数据,是否继续上次操作? 是[Y] 否[N] "):
            with open('content.pickle', 'rb') as f:
                内容 = pickle.load(f)
            with open('images.pickle', 'rb') as f:
                图片URL集合 = pickle.load(f)
            with open('info.pickle', 'rb') as f:
                书名, 作者, 封面URL = pickle.load(f)
        else:
            os.remove("content.pickle")
            os.remove("images.pickle")
            os.remove("info.pickle")
            主要()
    else:
        主要()
    
    #console.print(图片URL集合)
    下载图片集合(图片URL集合, 4)
    下载文件(封面URL)
    写到书本(书名, 作者, 内容, "cover", "file/"+封面URL.split("/")[-1], "file")
    shutil.rmtree('file')
    os.remove("content.pickle")
    os.remove("images.pickle")
    os.remove("info.pickle")
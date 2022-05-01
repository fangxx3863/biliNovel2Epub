# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import sys
import shutil
from rich.console import Console
from ebooklib import epub
import uuid
import download
from download import download
import ssl
from PIL import Image
import io
from multiprocessing import Process, Pool

console = Console()
session = requests.Session()
# 关闭SSL证书验证
ssl._create_default_https_context = ssl._create_unverified_context
# 初始化epub工具
book = epub.EpubBook()

基础URL = "https://w.linovelib.com"

HEARDERS = {
    "cookie": "_ga=GA1.2.373713668.1646927652; _gid=GA1.2.1447053390.1651231171; Hm_lpvt_d29ecd95ff28d58324c09b9dc0bee919=1651231349; Hm_lvt_d29ecd95ff28d58324c09b9dc0bee919=1649823562,1651231165; jieqiUserInfo=jieqiUserId%3D627182%2CjieqiUserUname%3Dfangxx3863%2CjieqiUserName%3Dfangxx3863%2CjieqiUserGroup%3D3%2CjieqiUserGroupName%3D%E6%99%AE%E9%80%9A%E4%BC%9A%E5%91%98%2CjieqiUserVip%3D0%2CjieqiUserHonorId%3D1%2CjieqiUserHonor%3D%E5%A4%A9%E7%84%B6%2CjieqiUserToken%3D8ea5ef793d94938673124b15cb3a7102%2CjieqiCodeLogin%3D0%2CjieqiCodePost%3D0%2CjieqiUserPassword%3D5c82b131f01843ca05e751717d74a992%2CjieqiUserLogin%3D1651231169; jieqiVisitId=article_articleviews%3D2939; jieqiVisitInfo=jieqiUserLogin%3D1651231169%2CjieqiUserId%3D627182; night=0; PHPSESSID=bsdrsrdj916v5etol006ji2odl",
    "referer": "https://w.linovelib.com/",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36",
}



def 标准化JSON(s:str)->dict:
    obj = eval(s, type('js', (dict,), dict(__getitem__=lambda s, n: n))())
    return obj


# 下载函数
def 下载文件(url, path='file'):
    if isinstance(url, str):
        try:
            download(url, os.getcwd() + '/' + str(path) + '/' + os.path.basename(url), replace=False, verbose=False)
        except:
            return url
    if isinstance(url, list):
        errUrls = []
        for i in url:
            try:
                download(i, os.getcwd() + '/' + str(path) + '/' + os.path.basename(i), replace=False, verbose=False)
            except:
                errUrls.append(i)
                return errUrls

def 下载图片集合(urls, jobs):
    pool = Pool(int(jobs))
    errUrls = pool.map(下载文件, urls)
    errUrls = sorted(list(filter(None, errUrls)))
    while errUrls:
        errUrls = 下载文件(errUrls)
    #print(errUrls)

def 写到书本(title, author, content, cover_name, cover_file, imgDir, folder=None):
    """写入内容至epub

    传入基本参数，并将其写出至epub

    Args:
        title (str): 书籍名称
        author (str): 作者名称
        content (str): 文章html内容
        cover_name (str): 封面名称
        cover_file (str): 封面路径
        imgDir (str): 引用图片路径
    """    
    book.set_identifier(str(uuid.uuid4()))
    book.set_title(title)
    book.set_language('zh')
    book.add_author(author)
    cover_type = cover_file.split('.')[-1]
    book.set_cover(cover_name + '.' + cover_type, open(cover_file, 'rb').read())
    
    写入内容 = ""
    book.spine = ["nav", ]
    IDS = -1
    for 卷名 in content:
        卷名标题 = "<h1>" + 卷名 + "</h1>"
        写入内容 = 写入内容 + 卷名标题
        book.toc.append([epub.Section(卷名), []])
        IDS += 1
        #print(写入内容)
        for 章节 in content[卷名]:
            单页 = epub.EpubHtml(title = 章节[0],
                       file_name = 章节[0] + ".xhtml",
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


if __name__ == "__main__":
    书籍ID = str(sys.argv[1]).split("/")[-1].split(".")[0]
    #console.print(书籍ID)

    # 获得书籍名称
    书籍首页URL = 基础URL + f"/novel/{书籍ID}.html"
    soup = BeautifulSoup(session.get(书籍首页URL,headers=HEARDERS).text, "lxml")
    书名 = soup.find("h2",{"class":"book-title"}).text
    作者 = soup.find("div",{"class":"book-rand-a"}).text[:-2]
    简介 = soup.find(id = "bookSummary").text
    console.print(简介)

    # 解析书籍目录部分,获取URL
    目录 = dict()
    封面URL = 基础URL + f"/files/article/image/2/{书籍ID}/{书籍ID}s.jpg"
    目录URL = 基础URL + f"/novel/{书籍ID}/catalog"
    soup = BeautifulSoup(session.get(目录URL,headers=HEARDERS).text, "lxml")
    章节数 = soup.find("h4",{"class": "chapter-sub-title"}).find("output").text
    远程目录 = soup.find("ol",{"id":"volumes"})
    目录集合 = 远程目录.find_all("li")
    缓存 = 目录集合[0].text
    子章节 = []
    #console.print(缓存)

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
    #console.print(目录)
    
    for 卷名 in 目录:
        for 章节 in 目录[卷名]:
            #console.print(章节)
            章节标题 = 章节[0]
            章节URL = 章节[1]

            # 处理目录中的错误链接
            if 章节[1] == "javascript:cid(0)":
                章节[1] = 下一个URL
                #console.print(目录)
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
                
    内容 = dict()
    图片URL集合 = []
    IDS = -1
    for 卷名 in 目录:
        console.print("卷: " + 卷名)
        for 章节 in 目录[卷名]:
            内容.setdefault(卷名, []).append([章节[0]])
            IDS += 1
            console.print("章节: " + 章节[0])
            #console.print(内容)
            缓存内容 = ""
            for 单章URL in 章节[1:]:
                soup = BeautifulSoup(session.get(单章URL,headers=HEARDERS).text, "lxml")
                图片集合 = soup.find_all("img")
                #console.print(图片集合)
                文章内容 = str(soup.find(id="acontent"))
                for 原始 in 图片集合:
                    图片URL集合.append(str(原始).split("src=\"")[-1][:-3])
                    替换 = "file/" + str(原始).split("src=\"")[-1][:-3].split("/")[-1]
                    #console.print(替换)
                    文章内容 = 文章内容.replace(str(原始).split("src=\"")[-1][:-3], str(替换))
                缓存内容 = 缓存内容 + 文章内容
                #console.print(内容)
                console.print(f"正在处理: {单章URL}")
            内容[卷名][IDS].append(缓存内容)

    #console.print(图片URL集合)
    #print(内容)

    下载图片集合(图片URL集合, 16)
    下载文件(封面URL)
    写到书本(书名, 作者, 内容, "cover", "file/"+封面URL.split("/")[-1], "file")
    shutil.rmtree('file')
# -*- coding: utf-8 -*-
import time
import requests
import pickle
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import sys
import shutil
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt
from rich.prompt import Confirm
from ebooklib import epub
import uuid
import ssl
from PIL import Image
import io
import re
from random import randint
from multiprocessing import Pool, set_start_method
import multiprocessing
#set_start_method('spawn', force=True)

console = Console()
session = requests.Session()
# 关闭SSL证书验证
ssl._create_default_https_context = ssl._create_unverified_context


基础URL = "https://w.linovelib.com"

 
USER_AGENTS =    ["Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
                  "Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
                  "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
                  "Mozilla/5.0 (Linux; Android 10; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
                  "Mozilla/5.0 (Linux; Android 4.3; Nexus 7 Build/JSS15Q) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                  "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.124 Mobile/15E148 Safari/604.1",
                  "Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.124 Mobile/15E148 Safari/604.1",
                  "Mozilla/5.0 (Android 4.4; Mobile; rv:70.0) Gecko/70.0 Firefox/70.0",
                  "Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) FxiOS/1.0 Mobile/12F69 Safari/600.1.4",
                  "Mozilla/5.0 (iPad; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) FxiOS/1.0 Mobile/12F69 Safari/600.1.4",
                  "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
                  "Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 EdgiOS/44.5.0.10 Mobile/15E148 Safari/604.1",
                  "Mozilla/5.0 (iPad; CPU OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 EdgiOS/44.5.2 Mobile/15E148 Safari/605.1.15",
                  "Mozilla/5.0 (Linux; Android 8.1.0; Pixel Build/OPM4.171019.021.D1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.109 Mobile Safari/537.36 EdgA/42.0.0.2057",
                  "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 7 Build/MOB30X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.109 Safari/537.36 EdgA/42.0.0.2057",
                  "Opera/12.02 (Android 4.1; Linux; Opera Mobi/ADR-1111101157; U; en-US) Presto/2.9.201 Version/12.02",
                  "Opera/9.80 (iPhone; Opera Mini/8.0.0/34.2336; U; en) Presto/2.8.119 Version/11.10",
                  "Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
                  "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
                  "Mozilla/5.0 (Linux; U; Android 8.1.0; en-US; Nexus 6P Build/OPM7.181205.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.11.1.1197 Mobile Safari/537.36",
                  "Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X; zh-CN) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/16B92 UCBrowser/12.1.7.1109 Mobile AliApp(TUnionSDK/0.1.20.3)",
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

def clean_file_name(filename:str):
    invalid_chars='[\\\:*?"<>|]'
    replace_char='-'
    return re.sub(invalid_chars,replace_char,filename)

# 下载函数
def 下载文件(链接, 路径='file'):
    if isinstance(链接, str):
        if "http" not in 链接:
            return
        if " " in 链接:
            return
        try:
            文件名 = "-"
            文件名 = 文件名.join(clean_file_name(链接).split("/")[-4:])
        except:
            return
        文件存在 = Path(f"{路径}/{文件名}")
        if 文件存在.exists():
            return
        try:
            请求 = requests.get(链接, headers=HEARDERS)
            # 检查文件完整性
            expected_length = 请求.headers.get('Content-Length')
            if expected_length is not None:
                actual_length = 请求.raw.tell()
                expected_length = int(expected_length)
                if actual_length < expected_length:
                    raise IOError(
                        'incomplete read ({} bytes read, {} more expected)'.format(
                            actual_length,
                            expected_length - actual_length
                        )
                    )
            
        except:
            try:
                os.remove(f"{路径}/{文件名}")
            except:
                pass
            return 链接
        console.print(f"正在下载: [dark_slate_gray2]{链接}[/dark_slate_gray2]")
        with open(f"{路径}/{文件名}", "wb") as f:
            f.write(请求.content)
    if isinstance(链接, list):
        错误链接 = []
        for i in 链接:
            if "http" not in 链接:
                continue
            if " " in 链接:
                return
            try:                            
                文件名 = "-"
                文件名 = 文件名.join(链接.split("/")[-4:])
            except:
                return
            文件存在 = Path(f"{路径}/{文件名}")
            if 文件存在.exists():   
                return
            try:
                请求 = requests.get(链接, headers=HEARDERS)
                
                # 检查文件完整性
                expected_length = 请求.headers.get('Content-Length')
                if expected_length is not None:
                    actual_length = 请求.raw.tell()
                    expected_length = int(expected_length)
                    if actual_length < expected_length:
                        raise IOError(
                            'incomplete read ({} bytes read, {} more expected)'.format(
                                actual_length,
                                expected_length - actual_length
                            )
                        )
            except:
                try:
                    os.remove(f"{路径}/{文件名}")
                except:
                    pass
                错误链接.append(i)
            console.print(f"正在下载: [dark_slate_gray2]{链接}[/dark_slate_gray2]")
            with open(f"{路径}/{文件名}", "wb") as f:
                f.write(请求.content)
        return 错误链接

def 下载图片集合(urls, jobs):
    进程池 = Pool(int(jobs))
    错误链接 = 进程池.map(下载文件, urls)
    错误链接 = sorted(list(filter(None, 错误链接)))
    while 错误链接:
        错误链接 = 下载文件(错误链接)

def 写到书本(title, 作者, 内容, 封面文件名, 封面文件, 图片路径, folder=None, 分卷输出=False):
    # 初始化epub工具
    book = epub.EpubBook()
    book.set_identifier(str(uuid.uuid4()))
    book.set_title(title)
    book.set_language('zh')
    book.add_author(作者)
    cover_type = 封面文件.split('.')[-1]
    book.set_cover(封面文件名 + '.' + cover_type, open(封面文件, 'rb').read())
    写入内容 = ""
    book.spine = ["nav", ]
    IDS = -1
    文件序号 = -1
    
    if not 分卷输出:
        for 卷名 in 内容:
            console.print("卷: " + 卷名)
            卷名标题 = "<h1>" + 卷名 + "</h1>"
            写入内容 = 写入内容 + 卷名标题
            book.toc.append([epub.Section(卷名), []])
            IDS += 1
            for 章节 in 内容[卷名]:
                console.print("章节: " + 章节[0])
                文件序号 += 1
                单页 = epub.EpubHtml(title = 章节[0],
                        file_name = f"{文件序号}.xhtml",
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
    else:
        console.print("卷: " + title)
        卷名标题 = "<h1>" + title + "</h1>"
        写入内容 = 写入内容 + 卷名标题
        book.toc.append([epub.Section(title), []])
        IDS += 1
        for 章节 in 内容:
            console.print("章节: " + 章节[0])
            文件序号 += 1
            单页 = epub.EpubHtml(title = 章节[0],
                    file_name = f"{文件序号}.xhtml",
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
    
    图片路径集 = os.listdir(图片路径)
    for 文件名 in 图片路径集:
        if not (".jpg" or ".png" or ".webp" or ".jpeg" or ".bmp") in str(文件名):
            continue
        文件类型 = 文件名.split('.')[-1]
        # 加载图片文件
        try:
            img = Image.open(图片路径 + '/' + 文件名)
        except:
            continue
        b = io.BytesIO()
        img = img.convert('RGB')
        img.save(b, 'jpeg')
        data_img = b.getvalue()

        文件名 = 文件名.replace('png', 'jpg')
        img = epub.EpubItem(file_name="file/%s" % 文件名,
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
    分卷输出 = False
    if len(sys.argv) == 1:
        if Confirm.ask("您未输入任何参数,请选择一个操作 进入交互模式[Y] 查看命令帮助[N] "):
            书籍ID = str(Prompt.ask("请输入书籍简介页面网址或直接输入书籍ID ")).split("/")[-1].split(".")[0]
        else:
            console.print("\n1. 请于命令行中进入到本项目路径\n2. 执行 python3 bilinovel2epub.py BookID \n3. BookID替换为书籍ID或书籍首页链接")
            os._exit(0)
    else:
        书籍ID = str(sys.argv[1]).split("/")[-1].split(".")[0]
    
    if Confirm.ask("是否分卷输出文件? 分卷[Y] 单文件[N] "):
        分卷输出 = True
    else:
        分卷输出 = False
    if Confirm.ask("是否下载图片? 下载[Y] 不下载[N] "):
        下载图片 = True
    else:
        下载图片 = False
    # 获得书籍名称
    书籍首页URL = 基础URL + f"/novel/{书籍ID}.html"
    soup = BeautifulSoup(session.get(书籍首页URL,headers=HEARDERS).text, "lxml")
    try:
        书名 = soup.find("h2",{"class":"book-title"}).text
        作者 = soup.find("div",{"class":"book-rand-a"}).text[:-2]
        简介 = soup.find(id = "bookSummary").text
        封面URL = str(soup.find("img")).split("src=\"")[-1][:-3]
    except:
        console.print("您可能输入了错误的URL或ID!", style="rgb(230,58,58)")
        os._exit(0)
    
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
    图片URL集合 = dict()
    # 图片URL集合.append(封面URL)
    IDS = -1
    for 卷名 in 目录:
        console.print("卷: " + 卷名, style="rgb(50,205,50)")
        图片URL集合.setdefault(卷名, []).append(封面URL)
        IDS = -1
        for 章节 in 目录[卷名]:
            内容.setdefault(卷名, []).append([章节[0]])
            IDS += 1
            console.print("章节: " + 章节[0], style="rgb(238,154,0)")
            缓存内容 = ""
            章节标题 = 章节[0]
            章节URL = 章节[1]

            # 处理目录中的错误链接
            if 章节[1] == "javascript:cid(0)":
                章节[1] = 下一个URL
            else:
                下一个URL = 章节[1]
                
            while True:
                for i in range(6):
                    if i >= 5:
                        console.print("[red]错误次数过多!已终止运行!")
                        os._exit(0)
                    try:
                        soup = BeautifulSoup(session.get(下一个URL,headers=HEARDERS,timeout=5).text, "lxml")
                    except:
                        console.print(f"第{i + 1}次请求失败,正在重试...")
                        time.sleep(3)
                    else:
                        break
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
                for i in range(6):
                    if i >= 5:
                        console.print("[red]错误次数过多!已终止运行!")
                        os._exit(0)
                    try:
                        soup = BeautifulSoup(session.get(单章URL,headers=HEARDERS,timeout=5).text, "lxml")
                    except:
                        console.print(f"第{i + 1}次请求失败,正在重试...")
                        time.sleep(3)
                    else:
                        break
                图片集合 = soup.find_all("img")
                文章内容 = str(soup.find(id="acontent"))
                for 原始 in 图片集合:
                    图片URL集合[卷名].append(str(原始).split("src=\"")[-1][:-3])
                    # 替换 = "file/" + str(原始).split("src=\"")[-1][:-3].split("/")[-1]
                    替换目标 = re.search(r"(?<=src=\").*?(?=\")", str(原始))
                    替换 = "-"
                    替换 = "file/" + 替换.join(替换目标.group().split("/")[-4:])
                    文章内容 = 文章内容.replace(str(替换目标.group()), str(替换))
                缓存内容 = 缓存内容 + 文章内容
                console.print(f"正在处理: {单章URL}")
            内容[卷名][IDS].append(缓存内容)
            
    with open('content.pickle', 'wb') as f:
        pickle.dump(内容, f)
    with open('images.pickle', 'wb') as f:
        pickle.dump(图片URL集合, f)      
    with open('info.pickle', 'wb') as f:
        pickle.dump([书名, 作者, 封面URL, 分卷输出, 下载图片], f)
    
    if 下载图片 and (not 分卷输出):
        文件存在 = os.path.exists("file") #判断路径是否存在
        if not 文件存在:
            # 如果不存在则创建目录
            os.makedirs("file")
        图片URL列表 = []
        for i in 图片URL集合:
            for j in range(0, len(图片URL集合[i])):
                图片URL列表.append(图片URL集合[i][j])
        下载图片集合(图片URL列表, 4)
    
    if 下载图片 and 分卷输出:
        try:
            os.makedirs(书名)
        except:
            pass
        for 卷名 in 内容:
            文件存在 = os.path.exists("file") #判断路径是否存在
            if not 文件存在:
                # 如果不存在则创建目录
                os.makedirs("file")
            下载图片集合(图片URL集合[卷名], 4)
            写到书本(书名+"_"+卷名, 作者, 内容[卷名], "-".join(clean_file_name(封面URL).split("/")[-4:]), "file/" + "-".join(clean_file_name(封面URL).split("/")[-4:]), "file", 书名, True)
            try:
                shutil.rmtree('file')
            except:
                pass
    else:
        文件存在 = os.path.exists("file") #判断路径是否存在
        if not 文件存在:
            # 如果不存在则创建目录
            os.makedirs("file")
        下载文件(封面URL)
        写到书本(书名, 作者, 内容, "-".join(clean_file_name(封面URL).split("/")[-4:]), "file/" + "-".join(clean_file_name(封面URL).split("/")[-4:]), "file")
    try:
        shutil.rmtree('file')
    except:
        pass
    os.remove("content.pickle")
    os.remove("images.pickle")
    os.remove("info.pickle")
    os._exit(0)
    

if __name__ == "__main__":
    multiprocessing.freeze_support()
    contentFile = Path("content.pickle")
    imagesFile = Path("images.pickle")
    if contentFile.exists() or imagesFile.exists():
        if Confirm.ask("检测到上次失败数据,是否继续上次操作? 是[Y] 否[N] "):
            with open('content.pickle', 'rb') as f:
                内容 = pickle.load(f)
            with open('images.pickle', 'rb') as f:
                图片URL集合 = pickle.load(f)
            with open('info.pickle', 'rb') as f:
                书名, 作者, 封面URL, 分卷输出, 下载图片 = pickle.load(f)
        else:
            os.remove("content.pickle")
            os.remove("images.pickle")
            os.remove("info.pickle")
            # 忽略上次失败数据
            主要()
    else:
        # 没有上次失败数据
        主要()
    
    # 处理上次失败数据
    
    #console.print(图片URL集合)
    文件存在 = os.path.exists("file") #判断路径是否存在
    if not 文件存在:
        # 如果不存在则创建目录
        os.makedirs("file")
    if 下载图片 and (not 分卷输出):
        图片URL列表 = []
        for i in 图片URL集合:
            for j in range(0, len(图片URL集合[i])):
                图片URL列表.append(图片URL集合[i][j])
        下载图片集合(图片URL列表, 4)
        
    if 下载图片 and 分卷输出:
        try:
            os.makedirs(书名)
        except:
            pass
        for 卷名 in 内容:
            文件存在 = os.path.exists("file") #判断路径是否存在
            if not 文件存在:
                # 如果不存在则创建目录
                os.makedirs("file")
            下载图片集合(图片URL集合[卷名], 4)
            写到书本(书名+"_"+卷名, 作者, 内容[卷名], "-".join(clean_file_name(封面URL).split("/")[-4:]), "file/" + "-".join(clean_file_name(封面URL).split("/")[-4:]), "file", 书名, True)
            try:
                shutil.rmtree('file')
            except:
                pass
    else:
        文件存在 = os.path.exists("file") #判断路径是否存在
        if not 文件存在:
            # 如果不存在则创建目录
            os.makedirs("file")
        下载文件(封面URL)
        写到书本(书名, 作者, 内容, "-".join(clean_file_name(封面URL).split("/")[-4:]), "file/" + "-".join(clean_file_name(封面URL).split("/")[-4:]), "file")
    try:
        shutil.rmtree('file')
    except:
        pass
    os.remove("content.pickle")
    os.remove("images.pickle")
    os.remove("info.pickle")

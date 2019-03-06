from bs4 import BeautifulSoup as bs
import urllib.request
import json
import requests
import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QToolTip, QComboBox, QPushButton
from PyQt5.QtGui import QFont


def get_gegu_new(index):
    if(os.path.isdir("个股要闻") == False):
        os.mkdir("个股要闻")
    print("开始爬取个股要闻...")
    url = "http://stock.eastmoney.com/a/cggdd"+"_"+str(index)+".html"
    html = urllib.request.urlopen(url).read()
    with open("./个股要闻/"+"个股要闻"+str(index)+".html", "wb") as f:
        print("爬取个股要闻列数:", index)
        f.write(html)
        f.close()
    print("个股要闻爬取结束...")


def get_gegu_new_info(index):
    content = open("./个股要闻/"+"个股要闻"+str(index)+".html", "rb").read()
    soup = bs(content, "lxml")
    title_get = soup.select("div p.title a")
    info_get = soup.select("div p.info")
    with open("./个股要闻/"+"个股要闻"+str(index)+".txt", "w", encoding='utf-8') as f:
        for i, j in zip(title_get, info_get):
            f.write(i.text)
            if(j.get('title') == None):
                f.write(j.text)
            else:
                f.write(j.get('title'))
    f.close()


def get_hangye_new(index):
    if(os.path.isdir("行业要闻") == False):
        os.mkdir("行业要闻")
    print("开始爬取行业要闻...")
    url = "http://stock.eastmoney.com/a/chydd"+"_"+str(index)+".html"
    html = urllib.request.urlopen(url).read()
    with open("./行业要闻/"+"行业要闻"+str(index)+".html", "wb") as f:
        print("爬取行业要闻列数:", index)
        f.write(html)
        f.close()
    print("行业要闻爬取结束...")


def get_hangye_new_info(index):
    content = open("./行业要闻/"+"行业要闻"+str(index)+".html", "rb").read()
    soup = bs(content, "lxml")
    title_get = soup.select("div p.title a")
    info_get = soup.select("div p.info")
    with open("./行业要闻/"+"行业要闻"+str(index)+".txt", "w", encoding='utf-8') as f:
        for i, j in zip(title_get, info_get):
            f.write(i.text)
            if(j.get('title') == None):
                f.write(j.text)
            else:
                f.write(j.get('title'))
    f.close()


def get_gegu_yanbao(index):
    print("开始爬取个股研报...")
    api = "http://datainterface.eastmoney.com//EM_DataCenter/js.aspx?type=SR&sty=GGSR&js=var%20cyczwawu=" \
          "{%22data%22:[(x)],%22pages%22:%22(pc)%22,%22update%22:%22(ud)%22,%22count%22:%22(count)%22}&ps=50&p="+str(index)+"&mkt=0&stat=0&cmd=3"
    if(os.path.isdir("个股研报") == False):
        os.mkdir("个股研报")
    data = requests.get(api)
    respons_json = data.content.decode()
    respons_json = respons_json.replace("var cyczwawu=", "")
    dict_json = json.loads(respons_json)
    json_data = dict_json['data']
    with open('./个股研报/' + '个股研报'+str(index)+'.json', 'w', encoding='utf-8') as f:
        print("爬取个股研报列数:", index)
        f.write(json.dumps(json_data, ensure_ascii=False))
    print("爬取个股研报结束")


def get_gegu_yanbao_info(index):
    with open("./个股研报/个股研报"+str(index)+".json", 'r', encoding='utf8') as f:
        json_data = json.loads(f.read())
        print(json_data)
        text_data = []
        text_datas = []
        for i in range(1, 51):
            text_data.append(i)
            text_data.append(json_data[i-1]['datetime'][5:10])
            text_data.append(json_data[i-1]['secuFullCode'][0:6])
            text_data.append(json_data[i-1]['secuName'])
            text_data.append(json_data[i-1]['title'])
            text_data.append(json_data[i-1]['rate'])
            text_data.append(json_data[i-1]['change'])
            text_data.append(json_data[i-1]['insName'])
            text_data.append(json_data[i-1]['sys'][0])
            text_data.append(json_data[i-1]['syls'][0])
            text_data.append(json_data[i-1]['sys'][1])
            text_data.append(json_data[i-1]['syls'][1])
            text_datas.append(text_data)
            text_data = []
        with open("./个股研报/个股研报"+str(index)+".txt", 'w', encoding='utf8') as f:
            for j in range(1, 51):
                f.write(str(text_datas[j-1]))
                f.write('\n')


def get_hangye_yanbao(index):
    print("开始爬取行业研报...")
    api = "http://datainterface.eastmoney.com//EM_DataCenter/js.aspx?type=SR&sty=HYSR&mkt=0&stat=0&cmd=2&code=&sc=&ps=50&p="+str(index)+"&" \
          "js=var%20OaNRyaMx={%22data%22:[(x)],%22pages%22:%22(pc)%22,%22update%22:%22(ud)%22,%22count%22:%22(count)%22}"
    if(os.path.isdir("行业研报") == False):
        os.mkdir("行业研报")
    data = requests.get(api)
    respons_json = data.content.decode()
    respons_json = respons_json.replace("var OaNRyaMx=", "")
    dict_json = json.loads(respons_json)
    json_data = dict_json['data']
    with open('./行业研报/' + '行业研报'+str(index)+'.json', 'w', encoding='utf-8') as f:
        print("爬取行业研报列数:", index)
        f.write(json.dumps(json_data, ensure_ascii=False))
    print("爬取行业研报结束...")



class Example(QWidget):

    def __init__(self):
        super().__init__()
        global str
        Example.str = "个股要闻"
        global index
        Example.index = '1'
        self.initUI()

    def initUI(self):
        combo = QComboBox(self)
        combo.addItem("个股要闻")
        combo.addItem("行业要闻")
        combo.addItem("个股研报")
        combo.addItem("行业研报")
        combo.move(50, 50)

        list_select = QComboBox(self)
        for i in range(1, 26):
            list_select.addItem(str(i))
        list_select.move(200, 50)

        QToolTip.setFont(QFont('SansSerif', 10))

        self.setToolTip('爬取东方财富网信息')

        btn = QPushButton('爬取', self)
        btn.setToolTip('点击爬取')
        btn.resize(btn.sizeHint())
        btn.move(110, 100)

        combo.activated[str].connect(self.onActivated_str)
        list_select.activated[str].connect(self.onActivated_index)
        btn.clicked.connect(self.on_click)

        self.setGeometry(500, 300, 300, 200)
        self.setWindowTitle('爬虫ui')
        self.show()

    def onActivated_str(self, text):
        Example.str = text
        print(Example.str)

    def onActivated_index(self, text):
        Example.index = text
        print(Example.index)

    def on_click(self):
        if(Example.str == "个股要闻"):
            get_gegu_new(Example.index)
            get_gegu_new_info(Example.index)
        if(Example.str == "行业要闻"):
            get_hangye_new(Example.index)
            get_hangye_new_info(Example.index)
        if(Example.str == "个股研报"):
            get_gegu_yanbao(Example.index)
            get_gegu_yanbao_info(Example.index)
        if(Example.str == "行业研报"):
            get_hangye_yanbao(Example.index)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    # ex.onActivated()
    sys.exit(app.exec_())

import re
import time
import xlwt
import requests
from lxml import etree
from bs4 import BeautifulSoup as bs

# 'User-Agent'：模拟浏览器访问
# 'Cookie'：模拟登录，绕过滑动拼图验证
baseURL = 'https://maoyan.com/board/4'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.42',
    'Cookie': '__mta=107315005.1665939224502.1665939224502.1665974803574.2; uuid_n_v=v1; uuid=173859204D7311ED85D65D754909B702076AF11DCDA544D8A900642BFA0187D6; _csrf=5432c7e2dc15d94264501c4618c9be1e08e65e61718496ecb14fa396186921fc; _lxsdk_cuid=183e1b733d2c8-0ea3069247b23a-4f6e117b-13c680-183e1b733d2c8; _lxsdk=173859204D7311ED85D65D754909B702076AF11DCDA544D8A900642BFA0187D6; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1665939224; __mta=121347895.1665974321686.1665974321686.1665974321686.1; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1665974803; _lxsdk_s=183e3cec045-f02-785-f64%7C%7C4'
}
s = requests.session()
s.keep_alive = False

def visit_page(url):
    page = s.get(url, headers=headers)
    print('accessing page: ', url)
    assert page and page.ok, '网页爬取失败'
    return bs(page.content, 'lxml')

# 从网页爬取数据
def scraping():
    # 获得全部页面信息存入列表中
    board_content_list = []
    for offset in range(10):
        board_url = baseURL + str(offset * 10)
        board_page = visit_page(board_url)
        board_content_list.append(board_page)
        time.sleep(0.5)
        with open(f'pages/offset_{offset}.html', 'w+', encoding='utf-8') as f:
            f.write(str(board_page.prettify()))
    return board_content_list


def download_image(url, name):
    img_format = re.findall('.jpg|.png|.webp', url)[0]
    with open('images/' + name + img_format, 'wb') as f:
        f.write(requests.get(url).content)


def process_metadata(metadta):
    movie_attrs = {
                'index':{'tag': 'i', 'class_':'board-index'}, 
                'name':{'tag': 'p', 'class_':'name'},
                'star':{'tag': 'p', 'class_':'star'}, 
                'releasetime':{'tag':'p', 'class_':'releasetime'},
                'integer':{'tag': 'i', 'class_':'integer'}, 
                'fraction':{'tag': 'i', 'class_': 'fraction'}
    }
                
    ret_info = {}
    for attr, attr_dict in movie_attrs.items():
        _info = metadta.find(attr_dict['tag'], class_=attr_dict['class_'])
        if not(attr == 'image'):
            _info = _info.text.strip()
        # else:
        #     download_image(url= _info['data-src'], title= _info['alt'])
        if attr in ('star', 'releasetime'):
            _info = re.split(':|：', _info)[1]
        ret_info[attr] = _info
    ret_info['score'] = ret_info.pop('integer') + ret_info.pop('fraction')
    return ret_info


# 处理数据
def batch_retrive_metadata(board_content_list):
    # 从页面上爬取每个电影的信息
    # index = [i for i in range(1, 101)]
    raw_movie_metadata = []

    for board_content in board_content_list:
        # for key in raw_info.keys():
        raw_movie_metadata += board_content.find_all('dd')
    
    processed_movie_metadata = [process_metadata(_) for _ in raw_movie_metadata]
    return processed_movie_metadata


# 将爬取到的数据存入Excel文件中
def build_excel_file(data):
    # 创建一个Excel文件
    f = xlwt.Workbook(encoding='UTF-8')
    # 创建一个sheet
    sheet1 = f.add_sheet(u'猫眼电影榜单Top100', cell_overwrite_ok=True)
    title = ['排名', '电影名称', '主演', '上映时间', '评分']
    # 写入列名
    for idx, t in enumerate(title):
        sheet1.write(0, idx, t)
    # 填写数据
    for idx, entry in enumerate(data):
        for k_idx, key in enumerate(entry.keys()):
            sheet1.write(idx, k_idx, entry[key])
    f.save('猫眼电影榜单Top100.xls')

def main():
    print("################程序运行开始################")
    print("<---------------开始爬取数据--------------->")
    board_html = scraping()
    print("<---------------数据爬取完成--------------->")
    print("<---------------开始处理数据--------------->")
    data = batch_retrive_metadata(board_html)
    print("<---------------数据处理完成--------------->")
    print("<---------------开始存储数据--------------->")
    print("将爬取数据存入Excel文件：")
    build_excel_file(data)
    print("<---------------数据存储完成--------------->")
    print("################程序运行结束################")

if __name__ == '__main__':
    main()

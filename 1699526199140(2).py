"""
    https://www.ncpssd.org/journal/list?page=1&t=0&s=0&h=%E7%BB%8F%E6%B5%8E%E7%AE%A1%E7%90%86&langType=1&clazz=C=F,C8,C9
    一共26页，只有page在变

    获取所有期刊的链接xpath://*[@id="form1"]/div[5]/div/div[2]/div/div[2]/ul/li[*]/a/@href
    ['/journal/details?gch=11118X&nav=1&langType=1', '/journal/details?gch=90379X&nav=1&langType=1', '/journal/details?gch=97894B&nav=1&langType=1', '/journal/details?gch=94953A&nav=1&langType=1', '/journal/details?gch=72338X&nav=1&langType=1', '/journal/details?gch=90140A&nav=1&langType=1', '/journal/details?gch=86074X&nav=1&langType=1', '/journal/details?gch=90151X&nav=1&langType=1', '/journal/details?gch=72005X&nav=1&langType=1', '/journal/details?gch=83282A&nav=1&langType=1', '/journal/details?gch=71362X&nav=1&langType=1', '/journal/details?gch=82827B&nav=1&langType=1', '/journal/details?gch=82456B&nav=1&langType=1', '/journal/details?gch=96682X&nav=1&langType=1', '/journal/details?gch=89577X&nav=1&langType=1', '/journal/details?gch=96009X&nav=1&langType=1', '/journal/details?gch=95598X&nav=1&langType=1', '/journal/details?gch=96436X&nav=1&langType=1', '/journal/details?gch=96813X&nav=1&langType=1', '/journal/details?gch=96218X&nav=1&langType=1']

"""
import random
import re
import time
from datetime import datetime
import requests
from lxml import etree
import hashlib

current_list = 4

user_agent_pool = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.6 (KHTML, like Gecko) Version/10.0 Mobile/14F89 Safari/602.1",
    "Mozilla/5.0 (iPad; CPU OS 10_3_2 like Mac OS X) AppleWebKit/603.2.6 (KHTML, like Gecko) Version/10.0 Mobile/14F89 Safari/602.1",
    "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.83 Mobile Safari/537.36",
]

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': 'Hm_lvt_a2e1dbec5d4200f69389a10a0dce981b=1698976616; web_session=d57ac4bc-2f3b-43a6-9d13-1bd4273fbd0e; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2218b92e5b4f8b1c-0c60d70d1dd4c5-26031151-2073600-18b92e5b4f9bcc%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%2218b92e5b4f8b1c-0c60d70d1dd4c5-26031151-2073600-18b92e5b4f9bcc%22%7D; Hm_lpvt_a2e1dbec5d4200f69389a10a0dce981b=1699320804',
    'Host': 'www.ncpssd.org',
    'Pragma': 'no-cache',
    'Referer': 'https://www.ncpssd.org/journal/list?p=1&e=&h=%E7%BB%8F%E6%B5%8E%E7%AE%A1%E7%90%86&langType=1&clazz=C%3DF%2CC8%2CC9',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': random.choice(user_agent_pool),
    'sec-ch-ua': '"Chromium";v="118", "Microsoft Edge";v="118", "Not=A?Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
}


def get_minio_sign():
    # 获取当前日期
    current_date = datetime.now()

    # 将日期格式化为"YYYY-MM-DD"形式
    formatted_date = current_date.strftime("%Y-%m-%d")
    # 注意在Python中字符串拼接使用'+'
    string_to_hash = 'L!N45S26y1SGzq9^' + formatted_date
    # 创建md5 hash对象
    hash_object = hashlib.md5(string_to_hash.encode())
    # 获取16进制哈希值
    sign = hash_object.hexdigest()
    return sign


headers_sign = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'ft.ncpssd.org',
    'Origin': 'https://www.ncpssd.org',
    'Referer': 'https://www.ncpssd.org/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'dotype': 'down',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sign': get_minio_sign(),
    'site': 'npssd',
    'userInfo': '5969474'
}


def get_session(username, password):
    url = "https://www.ncpssd.org/login"

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'Hm_lvt_a2e1dbec5d4200f69389a10a0dce981b=1698976616; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%225969474%22%2C%22first_id%22%3A%2218b92e5b4f8b1c-0c60d70d1dd4c5-26031151-2073600-18b92e5b4f9bcc%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%2218b92e5b4f8b1c-0c60d70d1dd4c5-26031151-2073600-18b92e5b4f9bcc%22%7D; web_session=e30ec01e-d988-4c24-951b-82fe1923afcb; Hm_lpvt_a2e1dbec5d4200f69389a10a0dce981b=1699343028',
        'Host': 'www.ncpssd.org',
        'Referer': 'https://www.ncpssd.org/login',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
    password_md5 = hashlib.md5(password.encode()).hexdigest()
    UrlReferrer = ""

    session = requests.Session()
    data = {
        "loginType": "account",
        "uname": username,
        "password": password_md5,
        "UrlReferrer": UrlReferrer
    }

    session.post(url=url, data=data, headers=headers).content.decode()
    return session


def clear_data(value):
    if type(value) == "None" or value == "" or value is None:
        value = ""
    return value


def get_years(url, headers):
    book_content = requests.get(url, headers=headers).content.decode()
    book_content_html = etree.HTML(book_content)
    xpath = book_content_html.xpath("//script/text()[contains(., 'list.push')]")[0]
    years = re.findall(r"list\.push\((.*?)\)", xpath)
    return book_content_html, years, xpath


def get_book_js(url, headers):
    book_content_html = get_years(url, headers)[0]
    xpath = book_content_html.xpath("//script/text()[contains(., 'list.push')]")[0]
    articleId_list_o = re.findall(r"articleIdList.push\((.*?)\)", xpath)
    articleId_list_n = [new_articleId.replace("'", "") for new_articleId in articleId_list_o]
    pdf_name_s_t = book_content_html.xpath('//div[@class="ct-detail"]//a[@id="a_down"]/@onclick')
    pdf_name_str = pdf_name_s_t[:int(len(pdf_name_s_t) / 3)]
    return pdf_name_str, articleId_list_n


def get_obj(url, headers):
    book_js_list = get_book_js(url, headers)[0]
    obj_list = []
    url_list = []
    for pdf_name_s in book_js_list:
        pdf_name_sp_list = pdf_name_s.split("(")[1].split(")")[0].split(",")
        obj = {}
        obj["type"] = pdf_name_sp_list[1].replace("'", "").replace(" ", "")
        obj["articleid"] = pdf_name_sp_list[2].replace("'", "").replace(" ", "")
        obj["periodname"] = pdf_name_sp_list[-1].replace("'", "").replace(" ", "")
        obj["downcount"] = pdf_name_sp_list[3].replace("'", "").replace(" ", "")
        obj["readcount"] = pdf_name_sp_list[4].replace("'", "").replace(" ", "")
        obj["gch"] = clear_data(pdf_name_sp_list[6].replace("'", "").replace(" ", ""))
        obj["class"] = clear_data(pdf_name_sp_list[7].replace("'", "").replace(" ", ""))
        obj["titleC"] = pdf_name_sp_list[8].replace("'", "").replace(" ", "")
        obj["showWriter"] = clear_data(pdf_name_sp_list[-2].replace("'", "").replace(" ", ""))
        obj["pageType"] = 1
        obj_list.append(obj)
        url_list.append(pdf_name_sp_list[5].replace("'", "").replace(" ", ""))
    return url_list


def get_real_url(url):
    page = 15
    # "https://www.ncpssd.org/journal/details?gch=83269X&years=2023&num=2&nav=1&langType=1"
    years = get_years(url, headers)[1]
    url_real = []
    print("获取可爬取期刊年限链接")
    for year in years:
        for i in range(1, page + 1):
            url_bok = url + f"&years={year}&num={i}"
            decode = requests.get(url=url_bok, headers=headers).content.decode()
            decode_html = etree.HTML(decode)
            check_str = decode_html.xpath('//*[@id="form1"]/div[6]/div/div[2]/div/p/text()')
            try:
                if check_str[0] == "暂无数据":
                    print(check_str)
                else:
                    url_real.append(url_bok)
                    print(url_bok)
            except Exception:
                print(check_str)
            time.sleep(random.randint(2, 5))
    return url_real


def get_pdf_one(url, headers, filepath, session, username, password):
    date_data = get_real_url(url)
    for date_url in date_data[20:]:
        print("*" * 200)
        print(datetime.now())
        print("获取链接")
        try:
            objs = get_obj(date_url, headers)
        except Exception:
            continue
        print(f"开始爬取:{date_url}")
        count = 1
        for key_url in objs:
            pdf_name = str(int(time.time())) + "op"
            kk_url = "https://www.ncpssd.org" + key_url + "&type=1"
            try:
                data_dic = session.get(kk_url).json()
            except Exception:
                print("cookie过期，重新登录")
                session = get_session(username, password)
                continue
            pdf_url = data_dic["url"]
            try:
                pdf_content = session.get(pdf_url, headers=headers_sign).content
                with open(f"{filepath}/{pdf_name}.pdf", 'wb') as f:
                    f.write(pdf_content)
                    print(f"第{count}个爬取成功")
                    f.close()
                    count += 1
                time.sleep(random.randint(2, 5))
            except Exception:
                print("链接超时")
                continue


if __name__ == '__main__':
    '''
        https://www.ncpssd.org/journal/index
        由于该网站内容很杂，所有需要自己复制期刊的链接
        url是该网站里面期刊的链接，修改url后可以开始下载期刊里面所有日期的期刊
        存储位置可以自己修改，修改filepath的值
        该网站需要登录，如果没有账号可以用我的，建议别用我的，自己注册账号
        该程序爬取率为95%，中间可能会由于网络或服务器问题缺失某个时期的部分期刊
        爬取的期刊会全部放到filepath文件里面，如给你需要分类，建议不要使用第二种循环方法
        pdf的名字是时间戳，所以不会重复
        以下是程序用到的包：
            import random
            import re
            import time
            from datetime import datetime
            import requests
            from lxml import etree
            import hashlib
    '''
    username = "xxxxxx"
    password = "xxxxxx"
    session = get_session(username, password)
    url = "https://www.ncpssd.org/journal/details?gch=97894B&nav=1&langType=1"
    filepath = "pdf17"

    # get_pdf_one(url, headers=headers, filepath=filepath, session=session,username,password)

    '''
        填写多个url后自动爬取,适合晚上爬取
    '''
    # 搜索链接https://www.ncpssd.org/journal/list?page=7&t=0&e=s=%E7%AE%A1%E7%90%86&c=&s=0&h=&langType=1&clazz=
    # 我的标记，1-7页可用期刊链接
    url_list = [
        "https://www.ncpssd.org/journal/details?gch=83809A&nav=1&langType=1",
        "https://www.ncpssd.org/journal/details?gch=81961X&nav=1&langType=1",
        "https://www.ncpssd.org/journal/details?gch=95764A&nav=1&langType=1",
        "https://www.ncpssd.org/journal/details?gch=90217X&nav=1&langType=1"
    ]
    for url in url_list:
        get_pdf_one(url, headers=headers, filepath=filepath, session=session, username=username, password=password)

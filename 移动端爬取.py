import requests
import time
import json



def get_url(max_id):
    """
    功能：获取下一个页面的url
    """
    url = f"https://m.weibo.cn/comments/hotflow?id=4693711642690158&mid=4693711642690158&max_id={max_id}&max_id_type=0"
    #5.9
    return url

def count():
    """
    功能：计算信息总数
    """
    global sum  #声明全局变量
    sum = sum +1
    print(sum)

def fetchURL(url):
    '''
    功能：访问 url 的网页，获取网页内容并返回
    参数：
        url ：目标网页的 url
    返回：目标网页的 html 内容
    '''

    headers = {
        "Accept": "application/json, textain, */*",
        "cookie": "SUB=_2A25MZp1_DeRhGeFP4lMS-CrMzj6IHXVvqCM3rDV6PUJbkdANLUn2kW1NQOuIwRcwlx3bH8fIYWhQVuHsqpvQQiyD; MLOGIN=1; WEIBOCN_FROM=1110006030; _T_WM=71174082094; XSRF-TOKEN=423bed; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D231583%26oid%3D4693704004079911%26uicode%3D10000011%26fid%3D100103type%253D1%2526t%253D10%2526q%253D%2523Uzi%25E6%25B1%2582%25E5%25A9%259A%25E6%2588%2590%25E5%258A%259F%2523",
        "Referer": "https://m.weibo.cn/detail/4693711642690158",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"

    }
    try:
        r = requests.get(url, headers=headers,timeout=31)
    except requests.HTTPError as e:
        print(e)
        print("HTTPError")
    except requests.RequestException as e:
        print(e)
    except:
        print("Unknown Error !")
    return r

def parse(resp,sum):
    """
    功能：解析网页，获取当前页内容，以及下页所需的max_id
    参数：网页内容，信息总数
    """
    s = json.loads(resp.text)
    try:
        max_id = s['data']["max_id"]
    except:
        pass

    try:
        for i in range(20):
            comment_content = s['data']['data'][i]["text"]
            comment_time = s['data']['data'][i]["created_at"]
            comment_like = s['data']['data'][i]["like_count"]
            if comment_content != []:
                count()
                print(comment_content)

    except:
        pass
    return max_id



if __name__ == '__main__':
    sum = 0  # 信息计数
    url = "https://m.weibo.cn/comments/hotflow?id=4693711642690158&mid=4693711642690158&max_id_type=0"
    for i in range(200):
        time.sleep(3)
        try:
            resp = fetchURL(url)
            time.sleep(30)
            max_id = parse(resp,sum)
            url = get_url(max_id)
            print(f"第{i+1}页")
        except:
            print("error")
    print('finish')

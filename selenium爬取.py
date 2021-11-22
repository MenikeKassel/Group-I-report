import time
from selenium import webdriver
import datetime
import os
import re

'''
获取所有内容发布的时间，以及标题
需要手动操作的部分为：
翻至底端，获取新闻页数，更改参数，
手动扫码登陆
用户姓名
'''


# 未解决问题：
# 1.有政治敏感词时，评论可见部分，但是点击没有反应。

def login():
    '''
    模拟登录
    '''
    driver.get('https://weibo.com/u/7191384052/home?leftnav=1')
    driver.maximize_window()
    time.sleep(5)
    login = driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[1]/div/a[2]')  # 找到安全登录按钮
    login.click()
    time.sleep(10)  # 手动扫码登录


def Transfer(driver):
    '''
    下拉滑动条，实现翻页功能
    '''
    try:
        driver.execute_script("window.scrollBy(0,document.body.scrollHeight)", "")  ## 移动到页面最底部
        time.sleep(2)
        driver.execute_script("window.scrollBy(0,document.body.scrollHeight)", "")
        time.sleep(2)
        driver.execute_script("window.scrollBy(0,document.body.scrollHeight)", "")
    except:
        pass
    return "Transfer successfully \n"


def get_more():
    """
    功能：点击微博底端查看更多页面
    """
    time.sleep(1)
    more = driver.find_element_by_xpath(
        f'//*[@id="Pl_Official_WeiboDetail__58"]/div/div/div/div[4]/div/div[3]/div[2]/div/div/a/span').click()
    # //*[@id="Pl_Official_WeiboDetail__58"]/div/div/div/div[4]/div/div[3]/div[2]/div/div/a/span
    #
    time.sleep(1)


def clear(text):
    '''
    :param text: 原文本
    :return: 清洗后的评论文本
    '''
    comment = re.findall('[a-zA-Z0-9_\u4e00-\u9fa5]+', text, re.S)  ## 文本预处理  去除一些无用的字符   只提取出中文出来
    comment_content = ','.join(comment[1::])  # 去掉冒号前面的用户名，将列表中的字符串拼接起来
    return comment_content


if __name__ == '__main__':
    driver = webdriver.Chrome()
    login()
    name = 'cctvxinwen'
    print('爬取的媒体用户名为：' + name)
    news_sum = 1
    start = 1
    end = 3297
    print(f"开始的页码为{start}")
    print(f"结束的页码为{end}")

    for news_page in range(start, end):  # 自己手动查看有多少页新闻#
        print(f"开始爬取第{news_page}页第{news_sum}条新闻")
        main_url = f'https://weibo.com/{name}?is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1&page={news_page}#feedtop'
        driver.get(main_url)
        Transfer(driver)  # 拉至底端
        Transfer(driver)

        for i in range(2, 47):
            try:
                news_comment_sum = driver.find_element_by_xpath(
                    f'//*[@id="Pl_Official_MyProfileFeed__26"]/div/div[{i}]/div[2]/div/ul/li[3]/a/span/span/span/em[2]').text  # 获取新闻下方的评论数
                news_time = driver.find_element_by_css_selector(
                    f'#Pl_Official_MyProfileFeed__26 > div > div:nth-child({i}) > div.WB_feed_detail.clearfix > div.WB_detail > div.WB_from.S_txt2 > a:nth-child(1)').text  # 获取界面上所有新闻的时间
                ##Pl_Official_MyProfileFeed__26 > div > div:nth-child({i}) > div.WB_feed_detail.clearfix > div.WB_detail > div.WB_from.S_txt2 > a:nth-child(1)
                if news_time[0:2] == "今天" or news_time[-3:] == '分钟前':  # 规范今天的内容，将其转换成日期
                    day = datetime.datetime.today()
                    news_time = str(day.month) + '月' + str(day.day) + '日'
                else:
                    a = r'月(.*?)日'
                    b = r'(.*?)月'
                    month = re.findall(b, news_time)[0]
                    day = re.findall(a, news_time)[0]
                    news_time = str(month) + "月" + str(day) + '日'  # 只要日期即可
            except:
                pass
            try:
                news_name = driver.find_element_by_css_selector(
                    f'#Pl_Official_MyProfileFeed__26 > div > div:nth-child({i}) > div.WB_feed_detail.clearfix > div.WB_detail > div.WB_text.W_f14 > a.a_topic').text  ###号内为文件名

            except:
                news_name = driver.find_element_by_xpath(
                    f'//*[@id="Pl_Official_MyProfileFeed__26"]/div/div[{i}]/div[1]/div[4]/div[4]').text  # 遇到没有##的标题就用原内容
            print(news_time)
            print("新闻名称为" + news_name)
            try:  # 创建以日期为名的文件夹
                file_path = os.path.abspath(f"C:\\Users\\12973\\Desktop\\疫情\\{name}")
                file_name = file_path + "\\" + news_time
                os.makedirs(file_name)
            except:
                pass

            f = open(f"C:\\Users\\12973\\Desktop\\疫情\\{name}\\{news_time}\\{news_name}.txt", "a+")  # 创建以新闻名为名称的txt文件
            time.sleep(10)
            try:
                flash = driver.find_element_by_css_selector(
                    f'#Pl_Official_MyProfileFeed__26> div > div:nth-child({i}) > div.WB_feed_handle > div > ul > li:nth-child(3) > a > span')

                driver.execute_script("arguments[0].click();", flash)  # 点击每个新闻的评论
            except:
                flash = driver.find_element_by_css_selector(
                    f'#Pl_Official_MyProfileFeed__26 > div > div:nth-child({i}) > div.WB_feed_repeat.S_bg1 > div > div > div.repeat_list > div.list_box > div > a > span')

                driver.execute_script("arguments[0].click();", flash)  # 点击每个新闻的评论
            time.sleep(3)
            more_text = driver.find_element_by_css_selector(
                f'#Pl_Official_MyProfileFeed__26 > div > div:nth-child({i}) > div.WB_feed_repeat.S_bg1 > div > div > div.repeat_list > div.list_box > div > a > span')
            driver.execute_script("arguments[0].click();", more_text)  # 点击更多
            time.sleep(3)
            driver.switch_to.window(driver.window_handles[-1])  # 切换窗口
            time.sleep(1)
            x = 8
            try:
                comment = driver.find_element_by_xpath(
                    f'//*[@id="Pl_Official_WeiboDetail__58"]/div/div/div/div[4]/div/div[3]/div[2]/div/div/div[1]/div[2]/div[1]').text
                for new_page in range(1, 100):
                    Transfer(driver)
                    get_more()
            except:
                pass
            try:
                for n in range(1, int(news_comment_sum)):  # 评论数为新闻页面爬取数#1，2不固定
                    comment = driver.find_element_by_xpath(
                        f'//*[@id="Pl_Official_WeiboDetail__58"]/div/div/div/div[4]/div/div[3]/div[2]/div/div/div[{n}]/div[2]/div[1]').text
                    # //*[@id="Pl_Official_WeiboDetail__55"]/div/div/div/div[4]/div/div[3]/div[2]/div/div/div[2]/div[2]/div[1]
                    comment_content = clear(comment)
                    f.write(comment_content + '\n')
                    # 当58时，是登陆状态，70是未登录状态
            except:
                pass
            f.close()
            driver.close()  # 关闭当前页面
            driver.switch_to.window(driver.window_handles[-1])  # 切换窗口
            news_sum = news_sum + 1
    driver.close()

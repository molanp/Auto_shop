import requests, time, os
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from lxml import etree

cookie_data = {}

def login(): 
 global cookie_data
 email = str(input('输入邮箱：'))
 password = str(input('输入密码：'))
 try:
    driver=webdriver.Edge()
    url="https://lantian.pro"
    try:
        driver.get(url)
        WebDriverWait(driver, timeout=3)
    except:
        raise(TimeoutError("连接超时"))
    
    driver.find_element(By.NAME,'email').send_keys(email)
    driver.find_element(By.NAME,'password').send_keys(password)
    driver.find_element(By.XPATH,'//*[@id="email"]/form/div[4]/button').click()
    cookies = driver.get_cookies()
    for item in cookies:
        cookie_data[item['name']] = item['value']
    if 'login_error_log' in cookie_data:
        print("登录失败请重试")
        print(f'Cookie: {cookie_data}')
        driver.close()
        login()
        return 'FAILL'
    else:
        print('登录成功')
        driver.close()
        print(f'Cookie: {cookie_data}')
        return 'OK'
 except BaseException as e:
    print(f"ERROR:\n{e}")
    return 'FAILL'

def add():
    try:
        driver.find_element(By.XPATH,'//*[@id="addToCartBtn"]').click()
    except:
        time.sleep(1)
        add()

login = login()
while login == 'OK':
    print('准备获取商品信息：')
    time.sleep(2)
    html = etree.HTML(requests.get(f'https://lantian.pro/cart?fid=2').text)
    for i in range(10):
        count = html.xpath(f'/html/body/div[2]/div/div[2]/div/div[2]/div/div/div/div[{i}]/div/div[2]/div/pre[2]/text()')
        name = html.xpath(f'/html/body/div[2]/div/div[2]/div/div[2]/div/div/div/div[{i}]/div/div[1]/h5/text()')
        h1 = html.xpath(f'/html/body/div[2]/div/div[2]/div/div[1]/div[2]/div/div/div/div[1]/ul/li[@class="active"]/a/text()')
        h2 = html.xpath(f'/html/body/div[2]/div/div[2]/div/div[1]/div[2]/div/div/div/div[2]/ul/li/ul/li/a/text()')#[@class="active"]
        for e in count:
            e = e.strip('库存：').strip()
            if e == '0':
                print(f'{h1}-{h2}-商品: {name}=无库存=库存:{e}')
            else:
                print(f'{h1}-{h2}-商品: {name}=有库存=库存:{e}')
                print('发现库存商品，开始抢购')
                driver = webdriver.Edge()
                driver.get('https://lantian.pro/cart?fid=2')
                for cookie in cookie_data:
                    driver.add_cookie({
                    "domain":".lantian.pro",
                    "name":cookie,
                    "value":cookie_data[cookie],
                    "path":'/',
                    "expires":None
                    })
                driver.get("https://lantian.pro/cart?fid=2")
                WebDriverWait(driver, timeout=3)
                #选择商品
                driver.find_element(By.XPATH,f'/html/body/div[2]/div/div[2]/div/div[2]/div/div/div/div[{i}]/div/div[2]/div/div[3]/a').click()
                #点击试用
                driver.find_element(By.XPATH,f'//*[@id="addCartForm"]/div/div[1]/div[2]/div/div[1]/div/div/label[1]').click()
                time.sleep(5)
                #加入购物车
                add()
                time.sleep(1)
                #同意服务协议
                ActionChains(driver).move_to_element_with_offset(driver.find_element(By.XPATH,'//*[contains(text(),"同意")]'), -20, 3).click().perform()
                time.sleep(1)
                #立即付款
                driver.find_element(By.XPATH,'//*[@id="submit-form"]/div/div[2]/div/div/div[4]/div/div[2]/button').click()
                print(f'成功抢购商品【{name}】')
                os.system('pause')
                exit(0)

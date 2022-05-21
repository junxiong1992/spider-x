import requests

def get_proxy():
    return requests.get("http://45.66.128.140:5010/get/").json()

def delete_proxy(proxy):
    requests.get("http://192.168.1.17:5010/delete/?proxy={}".format(proxy))

def getHtml():
    # ....
    retry_count = 2
    proxy = get_proxy().get("proxy")
    print(f'当前代理ip为{proxy}')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}

    CHECK_URL = 'http://api.ipify.org'
    # while retry_count > 0:
    #     try:
    #         resp = requests.get(url=CHECK_URL,headers=headers)
    #         # 使用代理访问
    #         print(f'响应为{resp.text}')
    #     except Exception as e:
    #         print(e)
    #         retry_count -= 1


    resp = requests.get(url=CHECK_URL,headers=headers)
    # 使用代理访问
    print(f'响应为{resp.text}')

    # 删除代理池中代理
    delete_proxy(proxy)
    return None

# proxy=get_proxy().get("proxy")
proxy=get_proxy().get("proxy")
print("Get Proxy IP:",proxy)
getHtml()
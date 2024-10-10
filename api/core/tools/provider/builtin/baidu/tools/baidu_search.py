import requests
from bs4 import BeautifulSoup

def search_and_extract_links(keyword):
    search_url = f"https://www.baidu.com/s?wd={keyword}"
    
    # 设置请求头，避免被识别为爬虫
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    # 发送请求
    response = requests.get(search_url, headers=headers)
    
    # 检查请求是否成功
    if response.status_code == 200:
        # 解析 HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取标题和链接
        results = []
        for g in soup.find_all('div', class_='result'):
            title = g.find('h3')
            link = g.find('a', href=True)
            if title and link:
                results.append({
                    'title': title.text,
                    'link': link['href']
                })
        
        return results
    else:
        print("请求失败，状态码：", response.status_code)
        return []

# 用户输入关键字
keyword = input("请输入搜索关键字: ")
links = search_and_extract_links(keyword)

# 输出结果
for index, result in enumerate(links):
    print(f"{index + 1}. 标题: {result['title']}, 链接: {result['link']}")




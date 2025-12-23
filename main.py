import requests
from bs4 import BeautifulSoup
import csv

# 请求头，模拟浏览器访问
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# 爬取函数
def crawl_university_ranking():
    base_url = 'https://www.shanghairanking.cn/rankings/best-universities'
    page = 1
    all_universities = []  # 存储所有大学信息
    
    while True:
        # 构造分页URL（软科排名通过page参数分页）
        url = f'{base_url}?page={page}'
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f'第{page}页请求失败，状态码：{response.status_code}')
            break
        
        soup = BeautifulSoup(response.text, 'html.parser')
        # 定位大学信息的表格行
        tr_list = soup.select('.rk-table tbody tr')
        if not tr_list:  # 没有数据时停止翻页
            break
        
        print(f'正在爬取第{page}页数据...')
        for tr in tr_list:
            # 提取排名、学校名称、总分
            rank = tr.select_one('td:nth-child(1)').text.strip()
            name = tr.select_one('td:nth-child(2) a').text.strip()
            score = tr.select_one('td:nth-child(3)').text.strip()
            all_universities.append({
                '排名': rank,
                '学校名称': name,
                '总分': score
            })
        
        page += 1  # 翻到下一页
    
    # 将数据保存到CSV文件
    with open('university_ranking.csv', 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['排名', '学校名称', '总分'])
        writer.writeheader()
        writer.writerows(all_universities)
    print(f'爬取完成！共获取{len(all_universities)}所大学信息，已保存至university_ranking.csv')

if __name__ == '__main__':
    crawl_university_ranking()

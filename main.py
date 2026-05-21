import requests
import re
import os

# 你的4个M3U链接列表
M3U_URLS = [
    "https://raw.githubusercontent.com/gjjlovewhy-ipoh/astrotv/refs/heads/main/My%209xtream.m3u",
    "https://raw.githubusercontent.com/gjjlovewhy-ipoh/astrotv/refs/heads/main/MYTV.m3u",
    "https://raw.githubusercontent.com/gjjlovewhy-ipoh/astrotv/refs/heads/main/MY%20TEST.m3u",
    "https://raw.githubusercontent.com/gjjlovewhy-ipoh/astrotv/refs/heads/main/IPTV_%E5%90%88%E5%B9%B6_20260521_0802.m3u"
]

# 存储去重后的直播源
live_list = []
exist_urls = set()

def get_m3u_content(url):
    """获取M3U文本内容"""
    try:
        resp = requests.get(url, timeout=15)
        resp.encoding = "utf-8"
        return resp.text
    except Exception as e:
        print(f"获取失败: {url} | 错误: {e}")
        return ""

def parse_m3u(content):
    """解析M3U，提取频道名和播放地址"""
    # 匹配 #EXTINF:-1,tvg-name=频道名 后紧跟播放地址
    pattern = re.compile(r'#EXTINF:-1.*?,(.*?)\n(http.*?)\n')
    matches = pattern.findall(content, re.S)
    for name, url in matches:
        name = name.strip()
        url = url.strip()
        if url and url not in exist_urls:
            exist_urls.add(url)
            live_list.append(f"{name},{url}")

def save_to_txt():
    """保存整理到live.txt"""
    with open("live.txt", "w", encoding="utf-8") as f:
        f.write("# 自动整理直播源 | 每小时GitHub自动更新\n")
        f.write("# 格式：频道名,播放地址\n\n")
        for item in live_list:
            f.write(item + "\n")
    print(f"已导出 {len(live_list)} 条直播源到 live.txt")

if __name__ == "__main__":
    for url in M3U_URLS:
        print(f"正在抓取: {url}")
        content = get_m3u_content(url)
        if content:
            parse_m3u(content)
    save_to_txt()

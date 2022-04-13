import requests
import json
from bs4 import BeautifulSoup

#@auther : aoilzmvg
#python爬虫练手
headers1 = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'
}

headers2 = {
    'Range' : 'bytes=0-',
    'Referer' : 'https://www.bilibili.com/video/',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'
}

def get_urls(bv):
    sp = requests.get(url='https://www.bilibili.com/video/'+bv,headers=headers1)
    soup=BeautifulSoup(sp.text,'html.parser')
    a = (soup.find_all('script')[3]).string[20:]
    json_urls = json.loads(a)
    video_urls = json_urls['data']['dash']['video']
    audio_urls = json_urls['data']['dash']['audio']
    return video_urls,audio_urls

def check_url(video_urls,audio_urls):
    urls = []
    video_url = video_urls[3]['baseUrl']
    audio_url = audio_urls[0]['baseUrl']
    urls.append(video_url)
    urls.append(audio_url)
    return urls

def download(filename,url,bv):
    with open(filename,'wb') as f:
        sp1 = requests.get(url=url,headers=headers2)
        f.write(sp1.content)

if __name__ == '__main__':
    bv = input('请输入bv号：')
    headers2['Referer'] = headers2['Referer'] + bv
    video_urls,audio_urls = get_urls(bv)
    urls = check_url(video_urls,audio_urls)
    print('已获取视频地址')
    print('正在下载视频')
    download('video.m4s',urls[0],bv)
    download('audio.m4s',urls[1],bv)

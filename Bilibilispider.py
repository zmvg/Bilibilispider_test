import requests
import json
from bs4 import BeautifulSoup
import sys

#@auther : aoilzmvg
#python爬虫练手

headers1 = {   #  get html
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'
}

headers2 = {   # get byte file
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

def check_url(video_urls,audio_urls):    #  pick up the urls
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

def main():
    bv = sys.argv[1]
    headers2['Referer'] = headers2['Referer'] + bv
    video_urls,audio_urls = get_urls(bv)
    urls = check_url(video_urls,audio_urls)
    print('[+] get urls')
    print('[+] downloading video')
    download('video.m4s',urls[0],bv)
    download('audio.m4s',urls[1],bv)

if __name__ == '__main__':
    main()
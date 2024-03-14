import os
import time
import random
import shutil
import requests
from bs4 import BeautifulSoup

def ReadScheduler():
    if os.path.exists( f'media/file.mp4' ):
        if not os.path.exists( f'file.mp4' ):
            shutil.move( 'media/file.mp4', 'file.mp4' )
        return

    response = requests.get( 'https://efukt.com/wMzEjM/Hc0RHamdTZjhTN0EGZlBTN98lJx0zblRWa29DcoBnLt9GZuFmcv02bj5CdrVnZl9yL6M' )

    if response.status_code == 200:
        random_url = response.url

        response.close()

        videopage = requests.get( random_url )

        if videopage.status_code == 200:
            soup = BeautifulSoup(videopage.content, 'html.parser')

            video_thumbnails = soup.find_all('div', class_='videoplayer_contents')
            if video_thumbnails:
                c = str(random.choice(video_thumbnails))
                i = c.find('source src="') + len('source src="')
                f = c.find('"', i)
                full_video_url = c[i:f]

                if full_video_url:
                    print("Downloading ", full_video_url )
                    download = requests.get( full_video_url, stream=True)
                    with open( f'media/file.mp4', 'wb') as video_file:
                        shutil.copyfileobj(download.raw, video_file)
                        video_file.close()
                    del download
                else:
                    print("Exception obtaining full_video_url")
            else:
                print("Can't find class videoplayer_contents")
        else:
            print("Failing to obtain the page:", videopage.status_code)
    else:
        print("Failing to obtain the page:", response.status_code)
    print( f'Finish downloading.' )

if os.path.exists( f'media/file.mp4' ):
    os.remove( f'media/file.mp4' )

while True:
    ReadScheduler()
    time.sleep( 5 )
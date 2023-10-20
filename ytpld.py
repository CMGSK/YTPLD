import os
import time
import re

try:
    from pytube import Playlist, YouTube
except ModuleNotFoundError:
    print('Please install pytube for the program to work.')

def get_urls(pl):
    urls = []
    for link in Playlist(pl):
        urls.append(link)
    return urls


def download(pl, mp3, dir):
    forRetry = []
    if dir == '':
        dir = os.getcwd()
    print('Downloading... Please wait. If your playlist is very long this could take some time.')
    for i, link in enumerate(pl):
        try:
            yt = YouTube(link)
            vid = yt.streams.filter(only_audio=mp3).first()
            output = vid.download(output_path=dir)
            if mp3:
                name, _ = os.path.splitext(output)
                name = re.sub(r'/W+', '', name)
                os.rename(output, name + '.mp3')
        except:
            print(f'Couldnt download {i}')
            forRetry.append(link)
            continue
        print(f'Downloaded: {i+1}/{str(len(pl))}')
    print('Your playlist has been downloaded.')
    if len(forRetry) > 0:
        print('Do you want to retry the failed downloads? Y/N')
        if str(input()).upper() == 'Y':
            download(forRetry, mp3, dir)


print('YTPLD - Full YouTube playlist downloader')
print('Please input the full YouTube playlist URL.')
print('The default setting will download MP3, if you want the video, flag the URL like [URL] --Video')
print('The default destination will be the local directory of this executable. '
      'To choose your own location, flag the directory with [URL] --dir-[Desired directory]')

user_input = input()
splitter = user_input.split(' ')
mp3 = True
dir = ''
if '--video' in user_input:
    mp3 = False
if '--dir' in user_input:
    dir = user_input[user_input.find('--dir') + len('--dir_'):]
download(get_urls(splitter[0]), mp3, dir)

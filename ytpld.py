import os
import time

try:
    from pytube import Playlist, YouTube
except ModuleNotFoundError:
    print('Please install pytube for the program to work.')


###

def get_urls(pl):
    urls = []
    for link in Playlist(pl):
        urls.append(link)
    return urls


def download(pl, mp3, dir):
    if dir == '':
        dir = os.getcwd()
    print('Downloading... Please wait. If your playlist is very long this could take some time.')
    cnt = len(pl)
    i = 1
    for link in pl:
        yt = YouTube(link)
        vid = yt.streams.filter(only_audio=mp3).first()
        output = vid.download(output_path=dir)
        if mp3:
            name, _ = os.path.splitext(output)
            try:
                os.rename(output, name + '.mp3')
            except: 
                #this supposedly wont be used, try is only used to bypass some in cmd usage
                #bug interaction between os.rename with YouTube.streams.download
                os.rename(output, '01'+name+'.mp3')
        print('Downloaded: {0}/{1}'.format(str(i), str(cnt)))
        i += 1
    print('Your playlist has been downloaded.')


###


print('YTPLD - Full YouTube playlist downloader')
print('Please input the full YouTube playlist URL.')
print('The default setting will download MP3, if you want the video, flag the URL like [URL] --Video')
print('The default destination will be the local directory of this executable. '
      'To choose your own location, flag the directory with [URL] --dir-[Desired directory]')

user_input = input()
splitter = user_input.split(' ')
mp3 = True
dir = ""
if '--Video' in user_input:
    mp3 = False
if '--dir' in user_input:
    dir = user_input[user_input.find('--dir') + len('--dir-'):]
download(get_urls(splitter[0]), mp3, dir)

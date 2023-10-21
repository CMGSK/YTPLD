import os
import time
import re

try:
    from pytube import Playlist, YouTube
except:
    import pip

    pip.main(['install', '--user', 'pytube'])
finally:
    try:
        from pytube import Playlist, YouTube
    except:
        print('Please install pytube manually for the program to work.')
        time.sleep(5)
        quit()


def get_urls(pl):
    urls = []
    for link in Playlist(pl):
        urls.append(link)
    return urls


def manageRenameExceptions():
    for name in os.listdir(os.getcwd()):
        if '.mp4' in name:
            if name[:-4] + '.mp3' in os.listdir(os.getcwd()):
                os.remove(os.getcwd() + name)


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
            print(f'Couldnt download {i + 1}')
            forRetry.append(link)
            continue
        print(f'Downloaded: {i + 1}/{str(len(pl))}')
    print('Your playlist has been downloaded.')
    if len(forRetry) > 0:
        manageRenameExceptions()
        print('The app has a slight chance of throw an error even tho the file has been downloaded successfuly \n'
              'due to youtube encodings. In this case, downloads will keep throwing an error\n')
        print('Do you want to retry the failed downloads? Y/N')
        if str(input()).upper() == 'Y':
            download(forRetry, mp3, dir)


print('YTPLD - Full YouTube playlist downloader\n\n'
      'Please input the full YouTube playlist URL.\n'
      'The default setting will download MP3, if you want the video, flag the URL like [URL] --video\n'
      'The default destination will be the local directory of this executable.\n'
      'To choose your own location, flag the directory with --dir [Desired directory]\n\n')

user_input = input()
splitter = user_input.split(' ')
mp3 = True
dir = ''
if '--video' in user_input:
    mp3 = False
if '--dir' in user_input:
    dir = user_input[user_input.find('--dir') + len('--dir_'):]
download(get_urls(splitter[0]), mp3, dir)

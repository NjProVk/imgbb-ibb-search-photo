import random

from proxy import *


def replaceName(named):
    if '"' in named:
        named = named.replace('"', '')
    if '*' in named:
        named = named.replace('*', '')
    if '?' in named:
        named = named.replace('?', '')
    if '\\' in named:
        named = named.replace('\\', '')
    if '/' in named:
        named = named.replace('/', '')
    if ':' in named:
        named = named.replace('"', '')
    if '<' in named:
        named = named.replace('<', '')
    if '>' in named:
        named = named.replace('>', '')
    if '|' in named:
        named = named.replace('|', '')

    return named


def GetRandomProxy():
    prox_send = ValidProxy[random.randint(0, len(ValidProxy)-1)]
    return [{'http': f'https://{prox_send}', 'https': f'http://{prox_send}'}, prox_send]


def GetPhoto(urls):
    req_photo = requests.get(f"https://i.ibb.co/{urls}", proxies=GetRandomProxy(), headers=faceH())
    if req_photo.status_code == 200:
        names = ''.join(
            [random.choice(list('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890')) for x in range(7)])
        valid_name = names+replaceName(urls.split('/')[1])
        with open(f'img/{valid_name}', 'wb') as file_save:
            file_save.write(req_photo.content)
        log(f"Save photo {urls.split('/')[1]} | https://i.ibb.co/{urls}")


if __name__ == '__main__':
    log('Start')
    index = 0
    all_thread = 0
    max_thread = 10
    try:
        while 1:
            all_thread += 1

            def Start_Bot():
                url = 'https://ibb.co/' + ''.join(
                    [random.choice(list('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890')) for x in
                     range(7)])
                global all_thread
                prx_sender = GetRandomProxy()
                try:
                    req = requests.get(url, proxies=prx_sender[0], headers=faceH(), timeout=10)
                    if req.status_code == 200:
                        GetPhoto(req.text.split('https://i.ibb.co/')[1].split('"')[0])
                except Exception as e:
                    if 'ProxyError' in str(e):
                        ValidProxy.remove(prx_sender[1])
                all_thread -= 1

            threading.Thread(target=Start_Bot()).start()

            while all_thread >= max_thread:
                if all_thread < max_thread:
                    os.system('cls')
                    print(f'Проверено {index} ссылок!')

    except Exception as e:
        log(traceback.format_exc(), 'ERROR')

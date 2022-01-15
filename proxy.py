import os
import traceback

import requests
import threading

from logger import log
from fakeHeaders import faceH
from bs4 import BeautifulSoup


with open('proxy.txt', 'w', encoding='utf-8') as c_c:
    pass

AllProxy = []
ValidProxy = []


def HideMe():
    global AllProxy
    hideM = []
    r = requests.get(
        f"https://hidemy.name/ru/proxy-list/?maxtime=300type=s#list", headers=faceH()
    )
    soup = BeautifulSoup(r.text, "html.parser")
    while 1:
        for date in soup.find_all("div", class_="table_block"):
            for tables in date.find_all("tbody"):
                for tresh in tables.find_all("tr"):
                    newer = ""
                    for prod in tables.find_all("td"):
                        try:
                            prod.text.split(".")[2]
                            newer = prod.text + ':'
                        except:
                            try:
                                int(prod.text)
                                newer = newer + prod.text
                                if newer in hideM:
                                    pass
                                else:
                                    hideM.append(newer)
                            except:
                                pass
        for nextslite in soup.find_all("div", class_="pagination"):
            vv_work = 0
            for next_page in nextslite.find_all("li", class_="next_array"):
                vv_work = 1
                page_next = str(next_page).split(";start=")[1].split("#list")[0]
                if next_page != "":
                    r = requests.get(
                        f"https://hidemy.name/ru/proxy-list/?maxtime=300&type=s&start={page_next}#list",
                        headers=faceH(),
                    )
                    soup = BeautifulSoup(r.text, "html.parser")
            if vv_work == 0:
                AllProxy = hideM
                return 'End!'


def FoxTools():
    global AllProxy
    FoxProxy = []
    try:
        r = requests.get("http://api.foxtools.ru/v2/Proxy", headers=faceH()).json()

        for items in r["response"]["items"]:
            good_ips = f"{items['ip']}:{items['port']}"
            if str(items["uptime"]).split(".")[0] <= "2":  #
                if str(items["type"]) == "1" or str(items["type"]) == "2":
                    if (
                            str(items["anonymity"]) != "None"
                            or str(items["anonymity"]) != "Unknown"
                            and str(items["anonymity"]) != "Low"
                    ):
                        FoxProxy.append(good_ips)
    except:
        pass
    AllProxy = FoxProxy


HideMe()
FoxTools()

index = 0
thd_all = 0
max_thd = 10

print(f'Start check == {len(AllProxy)} ips')

for get_prx in AllProxy:
    index += 1
    thd_all += 1

    # noinspection PyBroadException
    def thread_start(ips_proxy):
        global ValidProxy, thd_all
        try:
            r = requests.get('https://ibb.co', headers=faceH(), timeout=10)
            if r.status_code == 200:
                ValidProxy.append(ips_proxy)
        except Exception as e:
            log(traceback.format_exc(), 'ERROR')
        thd_all -= 1


    threading.Thread(target=thread_start, args=(get_prx,)).start()
    while thd_all >= max_thd:
        if thd_all < max_thd:
            os.system('cls')
            print(f'{index} == {len(AllProxy)}')


with open('proxy.txt', 'a', encoding='utf-8') as file:
    file.write(f"{list(ValidProxy)}")


import requests
import os
import time

url = 'https://www.pianolibrary.org/composers/'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0'
}

# nabere html, če še ni shranjen lokalno ga shrani, sicer pa ga nabere iz lokalne shrambe
def naberi_html(url_suffix):
    dat = f'./cache/{url_suffix}.html'
    
    if os.path.isfile(dat): # že imamo html
        with open(dat, 'r') as f:
            return f.read()
    
    odg = requests.get(url + url_suffix, headers=header)
    time.sleep(1) # da ne preobremenimo spletne strani

    if (odg.status_code != 200):
        print(f'Napaka {odg.status_code} pri dostopanju do spletne strani {url + url_suffix}.')
        return ''
    
    os.makedirs(os.path.dirname(dat), exist_ok=True) # če ne obstajajo mape, jih ustvari
    
    with open(dat, 'w') as f: # zapiši html na naš disk
        f.write(odg.text)

    return odg.text

#funkcije za našo spletno stran

def naberi_delo(priimek, naslov):
    return naberi_html(priimek + '/' + naslov)

def naberi_skladatelja(priimek):
    return naberi_html(priimek)

def naberi_skladatelje():
    return naberi_html('')
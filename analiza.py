import naberi
import razcleni
import json
import os

# funkcija, ki shrani vse html-je, ki jih rabimo, na disk
# prvič traja več kot uro; če je to predolgo, zmanjšaj čas spanja v naberi_html() v naberi.py

def naredi_cache():
    skladatelji = razcleni.seznam_skladateljev(naberi.naberi_skladatelje())

    for skladatelj in skladatelji:
        dela = razcleni.seznam_del(naberi.naberi_skladatelja(skladatelj[0]))
        for delo in dela:
            naberi.naberi_delo(skladatelj[0], delo)

# vrne podatke o skladateljih

def pridobi_skladatelje():
    return razcleni.seznam_skladateljev(naberi.naberi_skladatelje())

# vrne podatke o vseh skladbah
# če še niso tam, jih spravi v cache v datoteko podatki.json

def pridobi_skladbe():
    if os.path.isfile('podatki.json'):
        with open('podatki.json', 'r') as f:
                return json.load(f)
    
    naredi_cache()

    skladbe=[]
    for skladatelj in pridobi_skladatelje():
        dela = razcleni.seznam_del(naberi.naberi_skladatelja(skladatelj[0]))
        for delo in dela:
            skladbe.append(skladatelj + razcleni.podatki_o_delu(naberi.naberi_delo(skladatelj[0], delo)))

    with open('podatki.json', 'w') as f:
        json.dump(skladbe, f)
    
    return skladbe
import re
import html
import statistics

# iz HTML-ja glavne strani izlušči seznam tuplov (ID, ime, priimek, leto rojstva, leto smrti)
def seznam_skladateljev(html_skladateljev):
    seznam = re.findall(r'<tr><td><a href="./([^/]+)/index.html">([^<]+)<b>([^<]+)</b></a></td><td>(\d+)&ndash;(\d+)</td></tr>', html_skladateljev)

    # popravi trailing whitespace za imeni, spremeni HTML escape sequence nazaj v črke in spremeni letnice v števila
    return [(x[0], html.unescape(x[1].rstrip()), html.unescape(x[2]), int(x[3]), int(x[4])) for x in seznam]
    
# iz HTML-ja strani skladatelja izlušči seznam ID-jev del
def seznam_del(html_skladatelja):
    seznam = re.findall(r'<li><a href="./([^/]+)/index.html">', html_skladatelja)

    # izbriši podvojena dela
    return list(set(seznam))

# pretvori časovni format oblike 2' 30" v minute (2.5)
def trajanje_v_minutah(trajanje):
    trajanje = re.findall(r'\d+', trajanje)
    if len(trajanje) == 1:
        return float(trajanje[0])
    else:
        return float(trajanje[0]) + float(trajanje[1]) / 60

# če je v naslovu tonaliteta, jo izlušči v formatu {ton}-{lestvica}, kjer je ton predstavljen kot Ces, C, Cis, Des etc., lestvica pa je 'dur' ali 'mol'
def tonaliteta(naslov):
    # angleški format: {C, D, E, F, G, A, B} + (opcionalno) {-flat, -sharp} + {minor, major}
    toni = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
    modifierji = ['', '-flat', '-sharp']
    lestvice = [' minor', ' major']
    for ton in toni:
        for modifier in modifierji:
            for lestvica in lestvice:
                if naslov.lower().find(ton + modifier + lestvica) != -1:
                    # posloveni
                    if lestvica == ' minor':
                        lestev = ' mol'
                    else:
                        lestev = ' dur'

                    if ton == 'b':
                        if modifier == '-flat':
                            return 'B' + lestev
                        elif modifier == '-sharp':
                            return 'His' + lestev
                        else:
                            return 'H' + lestev
                    
                    if ton in 'ae' and modifier == '-flat':
                        return ton.upper() + 's' + lestev
                    
                    if modifier == '-flat':
                        return ton.upper() + 'es' + lestev
                    elif modifier == '-sharp':
                        return ton.upper() + 'is' + lestev
                    else:
                        return ton.upper() + lestev
    return None

# določi (zelo) približen tempo skladbe na podlagi naslova
def tempo(naslov):
    vrednosti = {'larghissimo': 16, 'largamente': 32, 'grave': 40, 
                 'molto adagio': 40, 'largo': 46, 'lento': 52, 
                 'adagio': 56, 'slow': 56, 'langsam': 56, 
                 'larghetto': 60, 'adagietto': 66, 'andante': 72, 
                 'andantino': 80, 'andante moderato': 83, 'maestoso': 88, 
                 'moderato': 92, 'moderate': 92, 'allegretto': 108, 
                 'animato': 120, 'allegro moderato': 128, 'allegro': 132, 
                 'fast': 132, 'schnell': 132, 'allegrissimo': 140, 
                 'molto allegro': 144, 'très vite': 144, 'vivace': 160, 
                 'vivacissimo': 168, 'presto': 184, 'prestissimo': 208}
    naslov = naslov.lower()
    tempi = [vrednost for marking, vrednost in vrednosti.items() if marking in naslov]
    
    if len(tempi) > 0:
        return statistics.mean(tempi)
    else:
        return None


# iz HTML-ja strani dela pridobi podatke o naslovu, približnem letu nastanka, skupnem trajanju in številu "poddel" (stavkov, variacij itd.)
# nato za vsak poddel dela pridobi podatke o naslovu, trajanju in težavnosti
# v naslovih so včasih podatki o tonaliteti in tempu delov; te poskusi izluščiti
def podatki_o_delu(html_dela):
    naslov = re.findall(r'<title>([^<]+)', html_dela)[0]

    # izbriši ime avtorja iz naslova dela
    for i in range(len(naslov) - 1, 0, -1):
        if naslov[i] == '(':
            naslov = naslov[:i - 1]
            break
    
    naslov = html.unescape(naslov)
    
    leto = re.findall(r'<h3 class="title">([^<]+)', html_dela)
    
    if len(leto) > 0:
        leto = html.unescape(leto[0])

        #upoštevamo samo števila s 4 števkami
        leto = [int(l) for l in re.findall(r'\d+', leto) if len(l) == 4]

        if len(leto) > 0:
            # če je navedenih več letnic, vzemimo kar povprečje
            leto = statistics.mean(leto)
        else: # leto nastanka ni podano
            leto = None
    else: # leto nastanka ni podano
        leto = None
    
    tezavnosti = [float(t) for t in re.findall(r'Difficulty: <a[^>]*>([^<]*)', html_dela)]
    tezavnost = max(tezavnosti) # težavnost dela je maksimum težavnosti komponent, ne povprečje

    # ali imamo opravka z večdelno kompozicijo? natanko za večdelne napišejo "Total duration"

    trajanje = re.findall(r'Total duration: ([^<]*)', html_dela)

    if len(trajanje) > 0:
        trajanje = trajanje_v_minutah(trajanje[0])

        naslovi = [html.unescape(n) for n in re.findall(r'<a href="#[^>]*>(.+?(?=</a>))', html_dela)]
        trajanja = [trajanje_v_minutah(t) for t in re.findall(r'Duration: ([^<]*)', html_dela)]

        return (naslov, leto, trajanje, tezavnost, tonaliteta(naslov), tempo(naslov),
                len(naslovi), naslovi, trajanja, tezavnosti, [tonaliteta(n) for n in naslovi], [tempo(n) for n in naslovi])
    else:
        trajanje = trajanje_v_minutah(re.findall(r'Duration: ([^<]*)', html_dela)[0])
        
        # to se zdi potratno, a olajša analizo
        return (naslov, leto, trajanje, tezavnost, tonaliteta(naslov), tempo(naslov),
                1, [naslov], [trajanje], tezavnosti, [tonaliteta(naslov)], [tempo(naslov)])
        



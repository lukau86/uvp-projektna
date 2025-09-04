# Analiza klasičnega klavirskega repertoarja

S pomočjo podatkov iz spletne strani [pianolibrary.org](https://www.pianolibrary.org) izvedemo grobo analizo zgodovine najpomembnejših skladateljev in skladb za klavir.

Koda, ki nabere podatke iz spletne strani in jih spravi v cache, se nahaja v [naberi.py](naberi.py). Koda, ki iz teh HTML datotek izlušči zanimive podatke je v [razcleni.py](razcleni.py). [analiza.py](analiza.py) pa vsebuje wrapperje za vse te funkcionalnosti, ki jih nazadnje pokličemo v Jupyter Notebooku [main.ipynb](main.ipynb). V tem notebooku se seveda nahajajo grafi in krajši premisleki o nabranih podatkih.

Uporabnik mora imeti nameščene sledeče knjižnice: requests, pandas, matplotlib, scipy, numpy. Te namestimo z ukazom <code>pip install [ime knjižnice]</code>.

Za uporabo preprosto odprite [main.ipynb](main.ipynb) v poljubnem programu, ki zmore brati Jupyter Notebook datoteke. V prvem odseku kode v tem notebooku se (če jih še ni v mapi [cache](cache/) oziroma v datoteki [podatki.json](podatki.json)) iz interneta prenesejo potrebni podatki. Ta proces na avtorjevem računalniku vzame približno uro časa.
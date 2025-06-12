Uvod:
Ovo su podaci o bruto investicijama u osnovna sredstva u Republici Srbiji. Osnova za podatke o bruto investicijama u osnovna sredstva je anketa o investicijama (INV01). INV01 obuhvata sva velika preduzeca i uzima uzorak malih i srednjih.

Fajl `s13.xlsx` predstavlja vremensku seriju od 1995. do 2023. godine bruto investicija u osnovna sredstva u sektoru drzave, ima 85 redova po godini koji predstavljaju delatnosti iz kojih je investirano i 35 kolona koje predstavljaju u sta je investirano.

Fajlovi `s1311.xlsx`, `s1313.xlsx` i `s1314.xlsx` predstavljaju vremenske serije od 2010. do 2023. godine za podsektore drzavnog sektora - (Javna preduzeca, Finansijski sektor, Zdravstvo valjda???)

Anketa o investicijama postoji i na nivou podsektora drzave, ali tek od 2010 godine. Prema Eurostatovim standardima trebaju da se imaju podaci za sve podsektore drzave od 1995. godine.

Tako da na osnovu podataka koje imamo o podsektorima od 2010 do 2023. godine, treba da se vrati serija do 1995. godine uz uslov da `np.all(s13 == s1311 + s1313 + s1314)`



Pristup:
Za godine za koje postoje podaci (2010 - 2023) za podsektore, izracunao sam udeo svakog podsektora u svakoj godini u svakoj delatnosti, onda sam iz tog skupa podataka izracunao prosek i standardnu devijaciju udela u odnosu na godine. Za prva dva podsektora generisao random brojeve iz uniformne raspodele `(max(0, mean - std), min(1, mean + std))`, a poslednji podsektor sam izracunao kao `s13 - s1311 - s1313`. 

Ceo kod u [fajlu](./resenje/final.py) 

Svi brojevi korisceni u ovom projektu su izmisljeni i sluze iskljucivo u ilustrativne i edukativne svrhe. 
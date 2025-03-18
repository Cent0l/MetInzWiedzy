import numpy as np
import itertools


# funkcja pomocnicza do sprawdzania sprzeczności
def sprz(o1, o2, atr):
    return all(o1[a] == o2[a] for a in atr) and o1[-1] != o2[-1]


# funkcja pomocnicza do generowania kombinacji
def genkom(atr, n):
    return list(itertools.combinations(atr, n))


# funkcja pomocnicza do znajdowania pokrywanych pbiektów
def znpok(dane, o1, kom):
    return {j for j, o2 in enumerate(dane) if all(o2[a] == o1[a] for a in kom)}


# funkcja pomocnicza do tworzenia regul,
def utreg(i, o1, kom, pokakt):
    pokcount = len(pokakt)
    pokstr = f"[{pokcount}]" if pokcount > 1 else ""
    atrstr = ''.join(f'(a{a+1}={o1[a]})' for a in kom)
    return f"o{i+1}{atrstr} -> (d={o1[-1]}){pokstr}"


# glowny algorytm funkcji
def seqcov(plik):
    dane = np.loadtxt(plik, dtype=int)
    kol = dane.shape[1]
    # indeksy atrybutow
    atr = list(range(kol - 1))
    # znalezione reguly
    reg = []
    #pokryte obiekty, na razie zbior pusty
    pok = set()
    for ilatr in range(1, len(atr) + 1):
        for i, o1 in enumerate(dane):
            if i in pok:
                continue
            for kom in genkom(atr, ilatr):
                if i in pok or any(sprz(o1, o2, kom) for o2 in dane if not np.array_equal(o2, o1)):
                    continue
                pokakt = znpok(dane, o1, kom)
                pok.update(pokakt)
                regakt = utreg(i, o1, kom, pokakt)
                if regakt not in reg:
                    reg.append(regakt)
    return reg

plik = "macierz.txt"
reguly = seqcov(plik)
for r in reguly:
    print(r)

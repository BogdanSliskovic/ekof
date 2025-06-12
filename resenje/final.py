import pandas as pd
import numpy as np
import joblib
from itertools import islice

grupe = joblib.load('grupe.pkl')
kolone = joblib.load('kolone.pkl')

numericki_indeksi = [vrednost for lista in grupe.values() for vrednost in lista]

def load(df):
    df = pd.read_excel(df + '.xlsx', index_col=[0,1])
    df = df[kolone]
    df = df[df.index.get_level_values(1).isin(numericki_indeksi)]
    return df

podsektori = {}
for s in ['s1311', 's1313', 's1314']:
    podsektori[s] = load(s)
    
s13 = load('s13')
s13_2010_2023 = s13[s13.index.get_level_values(0) >= 2010]

statistike = {'mean': {}, 'std': {}}
for naziv, podsektor in podsektori.items():
    odnos = podsektor / s13_2010_2023
    mean = odnos.groupby(level=1).mean().fillna(0)
    std = odnos.groupby(level=1).std().fillna(0)
    statistike['mean'][naziv] = mean
    statistike['std'][naziv] = std

suma = sum(statistike['mean'].values())

##svi proseci se sabiraju u 1 ili su nula
assert np.all((np.isclose(suma, 0)) | (np.isclose(suma, 1)))

#sve std su vece od nula
assert np.all([np.all(statistike['std'][naziv] >= 0) for naziv in statistike['std'].keys()])

###genrisem vrednosti za udeo u totalnom sektoru za prethodnih 15 godina, samo za 2 podsektora a treci ce da bude ostatak
s1311_imputacije = None 
s1313_imputacije = None

np.random.seed(42)
for naziv, podsektor in islice(podsektori.items(), 2):
    mean = statistike['mean'][naziv]
    std = statistike['std'][naziv]
    temp = np.random.uniform(np.maximum(0, mean - std), np.minimum(1, mean + std), size = (15,85,35)) ## za 15 godina u nazad
    globals()[f'{naziv}_imputacije'] = temp


## suma ne sme da bude veca od 1
df = s1311_imputacije + s1313_imputacije
mask = df > 1
s1313_imputacije[mask] = s1313_imputacije[mask] - (df[mask] - 1)
df = s1311_imputacije + s1313_imputacije
assert np.all(df <= 1.00001), np.all(df >= 0)


### sada treba da se generisu vrednosti za s1314, koje su ostatak sektora s13
##Uzimam vrednosti za s13 za godine pre 2010 i stavljam ih u numpy niz
s13_1995_2009 = s13[s13.index.get_level_values(0) < 2010]
godine_pre = range(1995,2010)

s13_1995_2009 = np.stack([s13_1995_2009[s13_1995_2009.index.get_level_values(0) == (godine_pre[g])] for g in range(len(godine_pre))])
assert s13_1995_2009.shape == s1311_imputacije.shape == s1313_imputacije.shape == (15,85,35)

dict_s1314 = {}
for i,godina  in enumerate(godine_pre):   
    ##tamo gde je sektor nula, podsektori su nula
    maska = s13_1995_2009[i] == 0
    s1311_imputacije[i][maska] = 0
    s1313_imputacije[i][maska] = 0
    
    temp = np.zeros_like(s1311_imputacije[i])
    ##tamo gde je sektor nije nula, s1314 je ostatak
    maska = s13_1995_2009[i] > 0
    temp[~maska] = 1 - (s1311_imputacije[i][~maska] + s1313_imputacije[i][~maska])
    
    dict_s1314[godina] = temp

s1314_imputacije = np.stack([dict_s1314[g] for g in godine_pre])  
    
suma = s1311_imputacije + s1313_imputacije + s1314_imputacije
epsilon = 1e-6

assert np.all(np.less(suma,1 + epsilon)) and np.all(np.greater(suma, -epsilon))
###imamo odnose za sve podsektore i sve godine, sada treba da se pomozi sa vrednostima celog sektora s13

imputacije = {'s1311': s1311_imputacije, 's1313': s1313_imputacije, 's1314': s1314_imputacije}

for naziv, podsektor in imputacije.items():
    podsektor = (s13_1995_2009 * podsektor)
    podsektor = pd.DataFrame(podsektor.reshape(-1, 35), index=[np.repeat(godine_pre, 85), np.tile(numericki_indeksi, 15)], columns=kolone )
    podsektor.to_excel(f'{naziv}_imputacije.xlsx')
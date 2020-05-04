import json
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import datetime as dt
import numpy as np

with open("COVID-19/dati-json/dpc-covid19-ita-andamento-nazionale.json", "r") as jsonData:
    data = jsonData.read()
    
# leggi json in una struttura python
andamenti = json.loads(data)

# le colonne d' interesse
columns = ['data', 'ricoverati_con_sintomi', 'terapia_intensiva', 'totale_ospedalizzati', 'isolamento_domiciliare', 'totale_positivi', 'variazione_totale_positivi', 'nuovi_positivi', 'dimessi_guariti', 'deceduti', 'totale_casi', 'tamponi', 'casi_testati']

dati = {col: [] for col in columns}

# trasformazione in ina lista di dizionari, così da poter usare un dataframe pandas
for andamento in andamenti:
    for col in columns:
        dati[col].append(andamento[col])
        
df = pd.DataFrame(dati)
df["data"] = pd.to_datetime(df["data"], infer_datetime_format=True)
df["data"] = df["data"].dt.strftime("%d/%m")

df1 = df[['data', 'nuovi_positivi']]
df1['tamponi_giornalieri'] = df['tamponi'].diff()
df1['pos%'] = df1['nuovi_positivi']/df1['tamponi_giornalieri']

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

fig = plt.figure(figsize=(30,20))
ax = fig.gca(projection='3d')

X = np.arange(df['data'].size)
Y = df['totale_casi']
Z = df['nuovi_positivi']

ax.plot(X, Y, Z, linewidth=1, antialiased=True)
xLabel = ax.set_xlabel('\nGiorni', linespacing=3.2)
yLabel = ax.set_ylabel('\nCasi Totali', linespacing=3.1)
zLabel = ax.set_zlabel('\nNuovi Positivi', linespacing=3.4)
plt.title("Andamento CoViD-19 in Italia", loc="Center")
plt.show()

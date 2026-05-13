import os
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

os.makedirs("graficos", exist_ok=True)

#top 20 grados salida
df = pd.read_csv("top_salidas.csv").head(20).sort_values("Grado_Salida")
df.plot.barh(x="Nombre", y="Grado_Salida", figsize=(10, 7), legend=False)
plt.title("Top 20 grado de salida")
plt.savefig("graficos/top_grado_salida.png")
plt.close()

#top 20 grados entrada
df = pd.read_csv("top_entradas.csv").head(20).sort_values("Grado_Entrada")
df.plot.barh(x="Nombre", y="Grado_Entrada", figsize=(10, 7), legend=False)
plt.title("Top 20 grado de entrada")
plt.savefig("graficos/top_grado_entrada.png")
plt.close()

#distribuicion de grados
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
for ax, csv, col, titulo in [(axes[0], "top_salidas.csv",  "Grado_Salida",  "Grado salida"),(axes[1], "top_entradas.csv", "Grado_Entrada", "Grado entrada"),]:
    conteo = Counter(pd.read_csv(csv)[col])
    ax.scatter(conteo.keys(), conteo.values(), s=10)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_title(titulo)
plt.savefig("graficos/distribucion_grados.png")
plt.close()

#top 20 pagerank
df = pd.read_csv("top_pagerank.csv").head(20).sort_values("PageRank_Score")
df.plot.barh(x="Nombre_Articulo", y="PageRank_Score", figsize=(10, 7), legend=False)
plt.title("Top 20 PageRank")
plt.savefig("graficos/top_pagerank.png")
plt.close()

#scatterplot grado salida vs entrada
df_pr = pd.read_csv("top_pagerank.csv").head(200)
df_e  = pd.read_csv("top_entradas.csv")[["Id", "Grado_Entrada"]]
df    = df_pr.merge(df_e, left_on="ID_Nodo", right_on="Id")
plt.figure(figsize=(9, 6))
plt.scatter(df["Grado_Entrada"], df["PageRank_Score"])
plt.title("Grado de entrada vs PageRank")
plt.xlabel("Grado de entrada")
plt.ylabel("PageRank Score")
plt.savefig("graficos/scatter_entrada_pr.png")
plt.close()

#categorias mas frecuentes
cats = pd.read_csv("top_pagerank.csv").head(100)["Categorias"].dropna()
conteo = Counter(c.strip() for fila in cats for c in fila.split(",") if c.strip() != "sin categoria")
nombres, valores = zip(*conteo.most_common(15))
plt.figure(figsize=(11, 5))
plt.bar(range(len(nombres)), valores)
plt.xticks(range(len(nombres)), nombres, rotation=35, ha="right")
plt.title("Categorias mas frecuentes - Top 100 PageRank")
plt.savefig("graficos/categorias_pagerank.png")
plt.close()

print("Graficos generados correctamente.")

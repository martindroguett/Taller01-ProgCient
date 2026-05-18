<a href=wikipedia.org><img src=https://raw.githubusercontent.com/martindroguett/Taller01-ProgCient/main/imgs/Wikipedia_Banner.svg.png align="center" alt="Wikipedia" ></a>

<h1 align="center"> Taller 01 - Programación Científica </h1>

<p align = center>
<a href = "https://www.ucn.cl"><img alt="Static Badge" src="https://img.shields.io/badge/Universidad_Católica_del_Norte-orange"></a>
<a href = "https://eic.ucn.cl"> <img alt="Static Badge" src="https://img.shields.io/badge/Escuela_de_Ingeniería_Coquimbo-blue"></a>
</p>

## Introducción
El presente repositorio consiste en la implementación de un programa capaz de analizar los datos ofrecidos por Stanford Network Analysis Project ([SNAP](https://snap.stanford.edu/data/wiki-topcats.html)) y recopilados en [Kaggle](https://www.kaggle.com/datasets/wolfram77/graphs-snap-wiki), los cuales ofrecen información de la red de artículos de Wikipedia y sus conexiones a través de sus hipervínculos, además de las categorías a las que estos pertenecen. 


El objetivo principal del proyecto es construir un grafo dirigido con que permita extraer información de los artículos con la finalidad de encontrar patrones en la red, implementar un algoritmo de [PageRank](https://en.wikipedia.org/wiki/PageRank), y generar rankings y gráficos basándonos en distintas métricas como: **grafos de salida/entrada**, **centralidad y cercanía**, o **cardinalidad**.

## Instalación
1. Clonar el repositorio y entrar en la carpeta:
``` bash
git clone https://github.com/martindroguett/Taller01-ProgCient
```
2. Entrar en la raíz del proyecto:
```bash
cd Taller01-ProgCient
```
2. Crear el entorno __conda__ y descargar sus dependencias con el archivo __yaml__:
``` bash
conda env create -f environment.yml
```
3. Activar el entorno:
``` bash
conda activate Taller_01-PC-MD-LM-FR
```

## Preparación
1. Debido a la magnitud de datos, los datasets deben ser instalados manualmente desde [aquí](https://www.kaggle.com/datasets/wolfram77/graphs-snap-wiki) y agregados en un directorio llamado __dataset__, en la raíz del proyecto. Los datasets a instalar son:
    - wiki-topcats.mtx
    - wiki-topcats_Categories.mtx 
    - wiki-topcats_Category_names.txt 
    - wiki-topcats_pagenames.txt

## Ejecución
1. Ejecutar __main__:
``` bash
python main.py
```

## Estructura

```
Taller01-ProgCient
├── Readme.md
├── enviroment.yml
├── graficos.py
├── main.py
└── src
    ├── Domain
    │   ├── Category.py
    │   ├── Graph.py
    │   ├── Node.py
    │   └── __init__.py
    ├── Logic
    │   ├── Algorithms.py
    │   ├── CSVWritters.py
    │   ├── WikiLoader.py
    │   └── __init__.py
    ├── Spinner.py
    └── __init__.py
```

## Menú Principal
<img src=https://raw.githubusercontent.com/martindroguett/Taller01-ProgCient/main/imgs/Menu.png alt="Menu" width = 80% heigth = 80% align="center" >

## Integrantes
<table>
  <tr>
    <td align="center">
      <a href="https://github.com/martindroguett">
        <img src="https://github.com/martindroguett.png" width="100px;" alt="Martín Droguett" style="border-radius:50%"/>
        <br />
        <sub><b>Martín Droguett Robledo</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/lucvsss">
        <img src="https://github.com/lucvsss.png" width="100px;" alt="Nombre del Integrante 2" style="border-radius:50%"/>
        <br />
        <sub><b>Lucas Munizaga Mora</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/Fifthtaschenmesser4">
        <img src="https://github.com/Fifthtaschenmesser4.png" width="100px;" alt="Nombre del Integrante 3" style="border-radius:50%"/>
        <br />
        <sub><b>Francisco Romero Opazo</b></sub>
      </a>
    </td>
  </tr>
</table>
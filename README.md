# NYC-metro-flow-forecast
Predição de série temporal da entradas de pessoas no metro da cidade de New York

## Overview
Este trabalho apresenta uma análise dos dados do metrô de NYC e a construção de modelos de séries temporais para prever o número de pessoas que entrará em determinada parte desta rede em determinado intervalo de tempo. O metro de NYC conta com diversas segmentações, então a base conta com bastante informação. Mais informações sobre a rede pode ser encontrada em https://pt.wikipedia.org/wiki/Metropolitano_de_Nova_Iorque.

## Dados
Os dados estão separados por ano (exemplo: 2016.csv) e vão de 2010 à 2017. Segue informações originais da base:

**Field Description**

CA,UNIT,SCP,STATION,LINENAME,DIVISION,DATE,TIME,DESC,ENTRIES,EXITS

- CA = Control Area (A002)
- UNIT = Remote Unit for a station (R051)
SCP = Subunit Channel Position represents an specific address for a device (02-00-00)
- STATION = Represents the station name the device is located at
- LINENAME = Represents all train lines that can be boarded at this station Normally lines are represented by one character. LINENAME 456NQR repersents train server for 4, 5, 6, N, Q, and R trains.
- DIVISION = Represents the Line originally the station belonged to BMT, IRT, or IND
- DATE = Represents the date (MM-DD-YY)
- TIME = Represents the time (hhmmss) for a scheduled audit event
- DESc = Represent the REGULAR scheduled audit event (Normally occurs every 4 hours) 1. Audits may occur more that 4 hours due to planning, or troubleshooting activities. 2. Additionally, there may be a RECOVR AUD entry This refers to a missed audit that was recovered.
- ENTRIES = The comulative entry register value for a device
- EXIST = The cumulative exit register value for a device

### Dados externos
Foi utilizado uma base externa com informações dos feriados de NYC em 2016. A base está no [kaggle](https://www.kaggle.com/pceccon/nyc2016holidays).

## Abordagens para Forecast
Para realizar a previsão de série temporal foi realizado um tratamento nos dados, indexano em 1 dias de intervalo e outra abordagem em 4h. Após esse processamento, foram as seguintes técnicas:
### Prophet
[Prophet](https://facebook.github.io/prophet/) é um framework do facebook para automatizar o treinamento de modelos para séries temporais. A implementação conta com modelos aditivos para capturar tendência não-lineares, sazonalidade, etc.

### Feature Engineering + Machine Learning
Essa abordagem consiste em construir features que estejam relacionadas com aspectos temporais, com informações históricas da série, data/hora, etc, e depois utilizar modelos de Regressão para prever a série temporal. Exemplo da abordagem na imagem abaixo em comparação com a forma tradicional de prever séries temporais.

![FeatureEngineeringML](reports/images/feature_engineering_ml.png)

## Como executar o projeto
```
git clone https://github.com/miltongneto/NYC-metro-flow-forecast/
cd NYC-metro-flow-forecast
pip install -r requirements.txt
jupyter notebook 
```

## Notebooks
A seguir uma breve explicação dos objetivos dos notebooks construídos na ordem (sugerida) para análise:

- [Análise Exploratória de Dados (eda.ipynb)](notebooks/eda.ipynb). Notebook de análise dos dados, voltado para entender os dados e séries, distribuição, além de realizar uma parte da preparação e limpeza dos dados.
- [Forecast com dados de 2016](notebooks/forecast.ipynb). Notebook com predição de série temporal com uma amostra de 2016. Utiliza o Prophet e técnicas de Feature Engineering. 
- [Forecast com vários anos](notebooks/forecast_data_complete.ipynb). Este notebook utiliza a mesma estação que o experimento anterior, entretanto com mais dados. É realizado um tratamento dos dados e a parte da modelagem é aprofundada, fazendo o uso de mais modelos de machine learning e técnicas de validação para série temporal. 

## Resultados
Resultados nos conjuntos de teste. 
Obs: cada dataset teve seu conjunto de teste específico.

|Dataset         |R2        |RMSE      |
|----------------|----------|----------|
|1 ano           |0,82      |37,15     |
|vários anos     |0.7       |37,3      |

## Notas
> A pasta html dentro de notebooks ([notebooks/html/](notebooks/html/)) contém os arquivos no formato .html, facilitando a visualização sem precisar executar o notebook e mantendo os gráficos.

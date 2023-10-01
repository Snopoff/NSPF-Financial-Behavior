# NSPF-Financial-Behavior
---
Для запуска веб-приложения необходимо установить библиотеки `npm` и `yarn`:
```
apt-get install -y nodejs
npm install --global yarn 
```
Также необходимо поставить библиотеки для `Python`:
```
pip install plotly
pip install geopandas
```
Далее небходимо открыть в двух терминалах папки `Archive/hack` и `Archive/hack_back` и в обоих папках написать команду `yarn install`. После установок надо прописать следующие команды:
 - В папке `Archive/hack`: `yarn start`
 - В папке `Archive/hack_back`: `node index.js`
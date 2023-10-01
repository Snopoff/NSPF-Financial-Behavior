FROM ubuntu

RUN apt-get update && \
    apt-get install -y python3 && \
    apt-get install -y pip && \
    apt-get install -y nodejs && \
    pip install geopandas && \
    pip install plotly && \
    npm install --global yarn 

WORKDIR /app

COPY ./scripts .
COPY /data .
COPY package*.json ./
COPY index.js .

RUN yarn install
EXPOSE 3001

CMD ["node", "index.js"]
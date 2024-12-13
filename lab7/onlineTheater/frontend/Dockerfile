FROM node:20 as build-stage

WORKDIR /my-frontend

COPY . /my-frontend

RUN npm install -g @vue/cli

RUN npm install

EXPOSE 5173

CMD ["npm", "run", "dev"]



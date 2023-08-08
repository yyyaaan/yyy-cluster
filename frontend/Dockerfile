FROM node:lts-alpine

RUN npm install -g http-server

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

# set in docker compose or kubenetes manifests
# EXPOSE 8080
# CMD [ "http-server", "dist" ]
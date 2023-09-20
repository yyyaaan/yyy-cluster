# Yan Pan 2023
# build stage, theme image will be replaced 
# hotfix: lts-alpine
FROM node:18.17-alpine as build-stage

ENV VUE_APP_API_ROOT=/api

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
COPY ./theme.png ./src/assets/theme.png
RUN npm run build

# production stage
FROM nginx:stable-alpine as production-stage

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build-stage /app/dist /usr/share/nginx/html

# set in compose or kubernetes
# CMD ["nginx", "-g", "daemon off;"]

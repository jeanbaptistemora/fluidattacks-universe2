FROM node:16-alpine@sha256:3235326357dfb65f1781dbc4df3b834546d8bf914e82cce58e6e6b676e23 AS build

WORKDIR /usr/src/app

COPY --chown=node:node package*.json ./
RUN npm i
COPY --chown=node:node . .
USER node

EXPOSE 22

WORKDIR /usr/src/app
COPY --chown=node:node package*.json ./
COPY --chown=node:node --from=development /usr/src/app/node_modules ./node_modules
COPY --chown=node:node . .

RUN npm run build

ENV NODE_ENV production

RUN npm i --only=production && npm cache clean --force
USER node

EXPOSE 8081 53

EXPOSE 21/tcp

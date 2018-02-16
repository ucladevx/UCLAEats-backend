FROM node:9.5.0-alpine

RUN apk add -U python make gcc g++ bash

# create the working directory
RUN mkdir -p /app/dea-backend

COPY *.json /app/dea-backend/

RUN cd /app/dea-backend && \
    npm install --only=production 

WORKDIR /app/dea-backend
COPY . /app/dea-backend/

EXPOSE 5000
CMD ["npm", "migrate"]
CMD ["npm", "start"]


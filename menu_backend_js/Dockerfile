FROM node:9.5.0-alpine

RUN apk add -U python make gcc g++ bash tzdata

# create the working directory
RUN mkdir -p /app/dea-backend

COPY *.json /app/dea-backend/

RUN cd /app/dea-backend && \
    npm install 

WORKDIR /app/dea-backend
COPY . /app/dea-backend/
# Entrypoint script

EXPOSE 5000

CMD ["npm", "start"]

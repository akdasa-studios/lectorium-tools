FROM node:18

WORKDIR /tools
COPY package*.json ./
RUN npm install
COPY . .
CMD ["node", "index.js"]

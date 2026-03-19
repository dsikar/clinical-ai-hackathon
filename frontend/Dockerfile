FROM node:20-alpine AS dev
WORKDIR /app
ENV NODE_ENV=development
COPY frontend/package*.json ./
RUN npm install
COPY frontend/. ./

EXPOSE 3000
CMD ["npm", "run", "dev", "--", "-H", "0.0.0.0"]

FROM node:18-alpine

WORKDIR /app

# Install dependencies first for better caching
COPY package.json package-lock.json* ./
RUN npm ci

# Copy source code and build Next.js application
COPY . .
RUN npm run build

EXPOSE 3000

CMD ["npm", "run", "start"]

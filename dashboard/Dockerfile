# Step 1: Use an official Node.js runtime as a parent image
FROM node:20.17.0

LABEL maintainer="Javid" \
      project="NLP Similarity" \
      tool="React"

WORKDIR /app

COPY package*.json ./
RUN npm install --legacy-peer-deps

COPY . .

RUN npm run build

RUN npm install -g serve

CMD ["serve", "-s", "build"]

# Expose the port on which the app will run
EXPOSE 3000
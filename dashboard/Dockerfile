# Step 1: Use an official Node.js runtime as a parent image
FROM node:20.17.0

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy package files and install dependencies
COPY package*.json ./
RUN npm install --legacy-peer-deps

# Step 4: Copy the rest of the application code
COPY . .

# Step 5: Build the React app for production
RUN npm run build

# Step 6: Serve the app using a simple web server like serve or nginx
# Install serve globally to serve the build
RUN npm install -g serve

# Step 7: Specify the command to run the app
CMD ["serve", "-s", "build"]

# Expose the port on which the app will run
EXPOSE 3000
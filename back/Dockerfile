# Use an official Python runtime as a parent image
FROM python:3.12.5

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
#RUN pip install --upgrade --require-hashes -r requirements.txt --no-deps
#RUN pip install --no-cache-dir  -r requirements.txt
RUN pip install --no-cache-dir --timeout=1000 -r requirements.txt
#RUN pip install --upgrade --require-hashes -r requirements.txt --no-deps

# Copy the rest of the application code
COPY . .

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Use an official Python runtime as a parent image
FROM python:3.12.5

LABEL maintainer="Javid" \
      project="NLP Similarity" \
      tool="FastAPI"

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

RUN pip install --timeout=1000 -r requirements.txt

COPY . .

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

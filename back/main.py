from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
# import numpy as np
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
from fastapi.middleware.cors import CORSMiddleware
import os
import gdown
import requests
import pandas as pd
from sentence_transformers import SentenceTransformer



app = FastAPI()

# Assume some placeholder data for datasets
datasets = {
    "string": ["sentence1", "sentence2", "sentence3"],
    "dataset2": ["another sentence", "more data here", "last example"],
}

DATASET_URL = "1uax1CncimQU-_kWvNigBONyplVRdi7PX"  # id of wiki-sections-sentences url
FILE_PATH = "wiki-sections-sentences.csv"

# Global variables to store the dataset and embeddings
df = None
embeddings = None
model = None

def download_dataset():
    """Download the dataset if it does not exist."""
    if not os.path.exists(FILE_PATH):
        print(f"Dataset not found. Downloading from {DATASET_URL}...")
        response = gdown.download(id = DATASET_URL,  output= FILE_PATH, quiet=False)
        print("response : ",response)
        # if response.status_code == 200:
        #     with open(FILE_PATH, 'wb') as file:
        #         file.write(response.content)
        #     print("Download complete.")
        # else:
        #     raise Exception("Failed to download the dataset.")

def load_and_encode_dataset():
    """Load the dataset and encode sentences."""
    global df, embeddings, model

    # Load the dataset
    df = pd.read_csv(FILE_PATH, sep='\t')

    # Ensure the Sentences column exists
    if 'Sentences' not in df.columns:
        raise ValueError("The dataset does not contain a 'Sentences' column.")

    # Load the model
    model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')

    # Encode all sentences
    sentences = df['Sentence'].dropna().tolist()
    embeddings = model.encode(sentences, show_progress_bar=True)
    print("Sentences have been encoded.")

@app.on_event("startup")
def startup_event():
    """Run on startup to prepare the dataset and embeddings."""
    try:
        download_dataset()
        load_and_encode_dataset()
    except Exception as e:
        print(f"Error during startup: {e}")
        raise HTTPException(status_code=500, detail="Failed to prepare the dataset.")


# Define a request body structure
class SimilarityRequest(BaseModel):
    dataset: str
    querySentence: str
    kValue: int

origins = [
    "http://localhost:3000",  # Allow requests from this frontend
    # "https://your-frontend-domain.com",  # Add other domains as needed
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows requests from specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


@app.get("/find-similar-sentences")
def find_similar_sentences():



# Route for retrieving similar sentences
@app.post("/find-similar-sentences")
async def find_similar_sentences(request: SimilarityRequest):
    # Check if dataset exists
    if request.dataset not in datasets:
        raise HTTPException(status_code=404, detail="Dataset not found")

    print("request:")
    print(request)

    # Retrieve and process sentences
    sentences = datasets[request.dataset]
    sentences.append(request)  # Add query sentence for similarity checking

    # Vectorize sentences and calculate similarity
    # vectorizer = TfidfVectorizer().fit_transform(sentences)
    # vectors = vectorizer.toarray()
    # cosine_sim = cosine_similarity([vectors[-1]], vectors[:-1])[0]  # Skip last item

    # Get top k similar sentences
    # top_k_indices = cosine_sim.argsort()[-request.k:][::-1]
    # similar_sentences = [sentences[i] for i in top_k_indices]

    return [
            {"id":1,"sentence":"sentense1  jsfh f ehf hejfhs jkhf jdshfkhs kfjhsdkh flskdjhf skldh flksjdhf k","score":2.5},
            {"id":2,"sentence":"sentense2","score":1.2}
        ]

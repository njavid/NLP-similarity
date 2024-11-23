from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import numpy as np
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
from fastapi.middleware.cors import CORSMiddleware
import os
import requests
import pandas as pd

import torch
from sentence_transformers import SentenceTransformer, util
import gdown


app = FastAPI()

# Assume some placeholder data for datasets
datasets_sep = {
    "wiki": '\t',
    "tasnim": ','
}
datasets_col = {
    "wiki": 'Sentence',
    "tasnim": 'abstract'
}

models = {
    "bert-fa-base-uncased-wikitriplet": {
        "model":"'m3hrdadfi/bert-fa-base-uncased-wikitriplet-mean-tokens",
        "data":"bert-fa-base-uncased-wikitriplet",
    },
    "paraphrase-multilingual-mpnet":{
        "model":"sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
        "data":"mpnet"
    }
}

#download model once and save in local directory:
# paraphrase_multilingual_mpnet = SentenceTransformer("sentence-transformers/paraphrase-multilingual-mpnet-base-v2")
# paraphrase_multilingual_mpnet.save("resources/mpnet_local_model")

# Load the model from the local directory
global paraphrase_multilingual_mpnet


def get_similar_sentences(dataset_path,data_emb_path,model_path,query,k,sep,col):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("device = ",device)

    # Load the models and dataset:
    model = paraphrase_multilingual_mpnet
    model.to(device)
    embeddings = np.load(data_emb_path)
    corpus_embeddings = torch.from_numpy(embeddings).to(device)
    corpus_embeddings = util.normalize_embeddings(corpus_embeddings)
    print([query])
    query_embeddings = model.encode([query])
    query_embeddings = util.normalize_embeddings(torch.tensor(query_embeddings))

    hits = util.semantic_search(query_embeddings, corpus_embeddings,top_k=k)


    df =  pd.read_csv(dataset_path, sep=sep)
    result = []

    # Assuming df has 'corpus_id' as the index or you can access it via a column
    id = 0
    for hit in hits[0]:
        id +=1
        corpus_id = hit['corpus_id']
        score = hit['score']

        # Retrieve the sentence using corpus_id from df
        sentence = df.loc[corpus_id, col]
        result.append({"id":id,"sentence":sentence,"score":round(score, 2)})

        # Print or store the sentence with the score
        print(f"Corpus ID: {corpus_id}, Score: {score:.4f}, Sentence: {sentence}")

    return result


@app.on_event("startup")
def startup_event():
    global paraphrase_multilingual_mpnet
    """Run on startup to prepare the dataset and embeddings."""
    if not os.path.exists('resources'):
        os.makedirs('resources')
        print(f"Created folder: resources")

    # Check if the model is already downloaded
    model_path = os.path.join('resources', "mpnet_local_model")
    if not os.path.exists(model_path):
        print("Downloading and saving the model...")
        model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-mpnet-base-v2")
        model.save(model_path)
        paraphrase_multilingual_mpnet = SentenceTransformer("resources/mpnet_local_model")

        gdown.download(id="1uax1CncimQU-_kWvNigBONyplVRdi7PX" , output = 'resources/wiki.csv', quiet = False)
        gdown.download(id="1-9iPfsr8WdWbBouvcrd0mveEdfgUqyoc", output='resources/wiki_mpnet_embeddings.npy', quiet=False)
        gdown.download(id="1kDl1AGa5ngrsV7DIklgQMmZ03Fj5iykG", output='resources/tasnim.csv', quiet=False)
        gdown.download(id="1YS-TPIppsU_nY6E3Rja-uuqqj8Ncq3pt", output='resources/tasnim_mpnet_embeddings.npy', quiet=False)

        print(f"Model and data saves successfully!")
    else:
        print("Model already exists.")





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


# @app.get("/find-similar-sentences")
# def find_similar_sentences():



@app.post("/find-similar-sentences")
async def find_similar_sentences(request: SimilarityRequest):
    # Check if dataset exists
    if request.dataset not in datasets_sep:
        raise HTTPException(status_code=404, detail="Dataset not found")

    print("request:")
    print(request)

    # Retrieve model and data:
    model_names = models['paraphrase-multilingual-mpnet']
    dataset_name= 'resources/' + request.dataset+'.csv'
    data_emb_path = 'resources/'+request.dataset+'_'+model_names["data"]+'_embeddings.npy'
    model_path = model_names["model"]

    similars = get_similar_sentences(dataset_name,data_emb_path,model_path,
                                     request.querySentence,request.kValue,
                                     sep=datasets_sep[request.dataset],
                                     col=datasets_col[request.dataset])
    return similars





        # [
        #     {"id":1,"sentence":"sentense1  jsfh f ehf hejfhs jkhf jdshfkhs kfjhsdkh flskdjhf skldh flksjdhf k","score":2.5},
        #     {"id":2,"sentence":"sentense2","score":1.2}
        # ]

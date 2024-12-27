from fastapi import FastAPI, File, UploadFile, Query, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import docx
import torch
from sentence_transformers import SentenceTransformer, util

app = FastAPI()

models = {
    1:"paraphrase_multilingual_mpnet",
    2:"paraphrase_multilingual_MiniLM",
    3:"bert_fa_base_uncased_wikitriplet"
}

#download model once and save in local directory:
# paraphrase_multilingual_mpnet = SentenceTransformer("sentence-transformers/paraphrase-multilingual-mpnet-base-v2")
# paraphrase_multilingual_mpnet.save("resources/mpnet_local_model")



# Load the model from the local directory
paraphrase_multilingual_mpnet = SentenceTransformer("resources/mpnet_local_model")
bert_fa_base_uncased_wikitriplet = SentenceTransformer("resources/bert-fa-base-uncased-wikitriplet")
paraphrase_multilingual_MiniLM = SentenceTransformer("resources/paraphrase-multilingual-MiniLM")


def get_similar_sentences(data,query,k,model):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("device = ",device)

    # Load the models and dataset:
    model.to(device)

    # embeddings = np.load(data_emb_path)
    # data = torch.from_numpy(np.array(data)).to(device)
    data_embeddings = model.encode(data)
    data_embeddings = util.normalize_embeddings(torch.tensor(data_embeddings))
    # print([query])
    query_embeddings = model.encode([query])
    query_embeddings = util.normalize_embeddings(torch.tensor(query_embeddings))

    hits = util.semantic_search(query_embeddings, data_embeddings,top_k=k)


    # df =  pd.read_csv(dataset_path, sep=sep)
    result = []

    # Assuming df has 'corpus_id' as the index or you can access it via a column
    id = 0
    for hit in hits[0]:
        id +=1
        data_id = hit['corpus_id']
        score = hit['score']

        # Retrieve the sentence using corpus_id from df
        sentence = data[data_id]
        result.append({"id":id,"sentence":sentence,"score":round(score, 2)})

        # Print or store the sentence with the score
        print(f"Data ID: {data_id}, Score: {score:.4f}, Sentence: {sentence}")

    return result


# @app.on_event("startup")
# def startup_event():
#     global paraphrase_multilingual_mpnet
#     """Run on startup to prepare the dataset and embeddings."""
#     if not os.path.exists('resources'):
#         os.makedirs('resources')
#         print(f"Created folder: resources")
#
#     # Check if the model is already downloaded
#     model_path = os.path.join('resources', "mpnet_local_model")
#     if not os.path.exists(model_path):
#         print("Downloading and saving the model...")
#         model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-mpnet-base-v2")
#         model.save(model_path)
#         paraphrase_multilingual_mpnet = SentenceTransformer("resources/mpnet_local_model")
#
#         gdown.download(id="1uax1CncimQU-_kWvNigBONyplVRdi7PX" , output = 'resources/wiki.csv', quiet = False)
#         gdown.download(id="1-9iPfsr8WdWbBouvcrd0mveEdfgUqyoc", output='resources/wiki_mpnet_embeddings.npy', quiet=False)
#         gdown.download(id="1kDl1AGa5ngrsV7DIklgQMmZ03Fj5iykG", output='resources/tasnim.csv', quiet=False)
#         gdown.download(id="1YS-TPIppsU_nY6E3Rja-uuqqj8Ncq3pt", output='resources/tasnim_mpnet_embeddings.npy', quiet=False)
#
#         print(f"Model and data saves successfully!")
#     else:
#         print("Model already exists.")





# Define a request body structure
class SimilarityRequest(BaseModel):
    data: List[str]
    # querySentence: str
    kValue: int
    query_text: Optional[str] = Query(None, description="Text input"),
    query_file: Optional[UploadFile] = File(None, description="Upload a .txt or .docx file")
    model_num: Optional[int] = Query(None, description="0: all (Coming Soon ...),"
                                                       "1 or None: paraphrase_multilingual_mpnet,"
                                                       "2: ")


origins = [
    "*",  # Allow requests from this frontend
    # "https://your-frontend-domain.com",  # Add other domains as needed
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


# @app.get("/find-similar-sentences")
# def find_similar_sentences():



@app.post("/find-similar-sentences")
async def find_similar_sentences(request: SimilarityRequest):
    print("request:")
    print(request)

    data = request.data
    query = None

    if request.query_text:
        query = request.query_text

    elif request.query_file:
        file = request.query_file
        if file.content_type not in ["text/plain",
                                     "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            raise HTTPException(status_code=400, detail="Invalid file type. Only .txt and .docx are allowed.")

        if file.content_type == "text/plain":
            query = file.read().decode("utf-8")
        elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = docx.Document(file)
            query = "\n".join([paragraph.text for paragraph in doc.paragraphs])

    else:
        raise HTTPException(status_code=400, detail="can't get query text.")


    # Retrieve model:
    model = None
    if request.model_num is not None:
        print("request.model_num",request.model_num)
        if request.model_num==0:
            results = {}
            for model in models.values():
                results[model] = get_similar_sentences(data,query,request.kValue,globals()[model])
                print(results)
            return results
        else:
            model = globals()[models[request.model_num]]
    else:
            model = paraphrase_multilingual_mpnet


    similars = get_similar_sentences(data,query,request.kValue,model)
    return similars





        # [
        #     {"id":1,"sentence":"sentense1  jsfh f ehf hejfhs jkhf jdshfkhs kfjhsdkh flskdjhf skldh flksjdhf k","score":2.5},
        #     {"id":2,"sentence":"sentense2","score":1.2}
        # ]

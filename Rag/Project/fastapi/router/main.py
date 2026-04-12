from fastapi import APIRouter, Request, File, UploadFile, Form
from fastapi.templating import Jinja2Templates
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import gradio as gr
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.node_parser import TokenTextSplitter
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.ingestion import IngestionPipeline

load_dotenv()

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/AskMe",
    tags=["AskMe"]
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.get("/")
async def get_page(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})


@router.post("/upload")
async def upload_file(request: Request, file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return templates.TemplateResponse(
        "main.html", {"request": request, "message": "File uploaded successfully!"}
    )


@router.post("/search/")
async def search_file(request: Request, query: str = Form(...)):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return templates.TemplateResponse(
            "main.html", {"request": request, "error": "Missing OPENAI_API_KEY in .env"}
        )

    documents = SimpleDirectoryReader("uploads").load_data()


    Settings.embed_model = OpenAIEmbedding(api_key=api_key)
    Settings.llm = OpenAI(model="gpt-4o", temperature=0)
    Settings.chunk_size = 1024
    text_splitter = TokenTextSplitter()

    chroma_client = chromadb.EphemeralClient()

    chroma_collection = chroma_client.get_or_create_collection(name="ps-foo-rag")

    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

    pipeline = IngestionPipeline(
        transformations=[
            text_splitter,
            Settings.embed_model,
        ],
        vector_store=vector_store,
    )
    pipeline.run(documents=documents)

    vector_index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        embed_model=Settings.embed_model,
    )


    query_engine = vector_index.as_query_engine()

    result = query_engine.query(query)

    answer = str(result)

    return templates.TemplateResponse(
        "main.html",
        {"request": request, "query": query, "answer": answer},
    )
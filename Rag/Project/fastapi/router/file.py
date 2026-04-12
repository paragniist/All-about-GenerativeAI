from fastapi import APIRouter, Request, File, UploadFile
from fastapi.templating import Jinja2Templates
import os
from dotenv import load_dotenv
import importlib
from llama_index.core.settings import Settings
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import TokenTextSplitter
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core import VectorStoreIndex

# Load environment variables
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
    """Handle file uploads."""
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return templates.TemplateResponse("main.html", {"request": request})


@router.post("/search/")
async def search_file(request: Request, query: str):
    """Perform retrieval-augmented generation using OpenAI models."""
    user_query = query
    api_key = os.environ.get('OPENAI_API_KEY')

    try:
        # Import OpenAI LLM and embedding models dynamically
        OpenAI = importlib.import_module("llama_index.llms.openai").OpenAI
        OpenAIEmbedding = importlib.import_module("llama_index.embeddings.openai").OpenAIEmbedding
    except ModuleNotFoundError as e:
        return templates.TemplateResponse(
            "main.html",
            {
                "request": request,
                "error": f"Missing optional dependency: {e.name}. "
                         f"Please install the corresponding llama-index provider package."
            },
        )


    Settings.llm = OpenAI(model="gpt-4o-mini", api_key=api_key)
    embed_model = OpenAIEmbedding(model="text-embedding-3-small", api_key=api_key)

    documents = SimpleDirectoryReader("uploads/").load_data()
    text_splitter = TokenTextSplitter(chunk_size=1024)


    chroma_client = chromadb.EphemeralClient()
    chroma_collection = chroma_client.get_or_create_collection("rag")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

   
    pipeline = IngestionPipeline(
        transformations=[
            text_splitter,
            embed_model,
        ],
        vector_store=vector_store,
    )
    nodes = pipeline.run(documents)
    print(f"Ingested {len(nodes)} nodes")


    vector_store_index = VectorStoreIndex.from_vector_store(
        vector_store,
        embed_model=embed_model,
    )

    vector_query_engine = vector_store_index.as_query_engine(
        vector_store_query_mode="hybrid", alpha=0.9
    )

    response = vector_query_engine.query(query)

    return templates.TemplateResponse(
        "main.html",
        {"request": request, "query": query, "answer": response.response},
    )

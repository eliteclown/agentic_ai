# Use the canonical langchain imports to match modern package APIs
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import dotenv 
dotenv.load_dotenv()

pdf_path = r"C:\Users\KT\Desktop\Agentic-AI\05_rag\ME_PROJECT_YOUTUBE_TRANSCRIPT.pdf"

loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
docs = splitter.split_documents(docs)
print(f"Number of documents after splitting: {len(docs)}")
vectore_store = Chroma.from_documents(
    embedding=OpenAIEmbeddings(),
    documents=docs,
    collection_name="example_collection",
    persist_directory="./chroma_langchain_db"
)

# print("vector store created", vectore_store.get_collection("example_collection").count())
print("pdf loaded and processed into vector store")
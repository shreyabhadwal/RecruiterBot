from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
import os

os.environ["OPENAI_API_KEY"] = "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" #OpenAI Key

def get_pdf_data(doc_name): #Function which loads PDF files(Along with page numbers)
    f_doc_name = 'Resumes_PDFs/' + doc_name
    loader = PyPDFLoader(f_doc_name)
    pages = loader.load_and_split()
    return(pages)

def get_resumes():
    resume_path = 'Resumes_PDFs'
    sources = []
    dir_list = os.listdir(resume_path)
    for i in dir_list:
        sources.append(get_pdf_data(i))
    return sources

def get_chunks():
    sources  = get_resumes()
    source_chunks = []  #Creating chunks of the source documents    
    splitter = CharacterTextSplitter(separator=" ", chunk_size=1024, chunk_overlap=0)
    for source1 in sources: #For each of the source mentioned
        for source in source1: #Go to each page
            for chunk in splitter.split_text(source.page_content): #Chunk up the content in each page
                chunk = chunk + "Filename is " + source.metadata['source']
                source_chunks.append(Document(page_content=chunk, metadata=source.metadata))#Append it to source_chunks
    return source_chunks

def create_embeddings():
    source_chunks = get_chunks()
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(source_chunks, embeddings)
    vectorstore.save_local("faiss_index")

def load_vectorstore():
    vectorstore = FAISS.load_local("faiss_index", OpenAIEmbeddings())

if __name__ == "__main__":
    create_embeddings()



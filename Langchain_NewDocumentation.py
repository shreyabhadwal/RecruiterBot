from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain import OpenAI
from langchain.chains import ConversationalRetrievalChain
import pickle
import os

os.environ["OPENAI_API_KEY"] = "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" #OpenAI Key
resume_path = 'C:/Users/sbhadwal/SpecChat/Resumes/Resumes_PDFs/'
sources = []

def get_pdf_data(doc_name): #Function which loads PDF files(Along with page numbers)
    f_doc_name = 'C:/Users/sbhadwal/SpecChat/Resumes/Resumes_PDFs/' + doc_name
    loader = PyPDFLoader(f_doc_name)
    pages = loader.load_and_split()
    return(pages)

dir_list = os.listdir(resume_path)

for i in dir_list:
    sources.append(get_pdf_data(i))

source_chunks = []  #Creating chunks of the source documents    
splitter = CharacterTextSplitter(separator=" ", chunk_size=1024, chunk_overlap=0)
for source1 in sources: #For each of the source mentioned
    for source in source1: #Go to each page
        for chunk in splitter.split_text(source.page_content): #Chunk up the content in each page
            chunk = chunk + "Filename is " + source.metadata['source']
            source_chunks.append(Document(page_content=chunk, metadata=source.metadata))#Append it to source_chunks

embeddings = OpenAIEmbeddings()
docsearch = FAISS.from_documents(source_chunks, embeddings)

""" with open("search_index.pickle", "rb") as f:
    docsearch = pickle.load(f)
 """
qa = ConversationalRetrievalChain.from_llm(OpenAI(temperature=0), docsearch.as_retriever())

chat_history = [] #Maintain a list for recording the chat history

def print_answer(question): 
    global chat_history
    result = qa(  #Run the chain
        {"question": question, "chat_history": chat_history},
        )
    chat_history.append((question, result["answer"])) #Update the chat history with the question asked and the answer
    print(result)

    if len(chat_history)>=5:
        chat_history=chat_history[1:]

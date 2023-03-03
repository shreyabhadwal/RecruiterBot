from langchain.chains.qa_with_sources import load_qa_with_sources_chain  
from langchain.chains.question_answering import load_qa_chain
from langchain.docstore.document import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain.llms import OpenAI
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import PagedPDFSplitter
from langchain.prompts import PromptTemplate
from langchain.chains.conversation.memory import ConversationBufferMemory
import os

os.environ["OPENAI_API_KEY"] = "" #Open AI Key

def get_text_data(doc_name):  #Function which loads text files 
    f_doc_name = doc_name + ".txt"
    loader = DirectoryLoader('C:/Users/sbhadwal/SpecChat/Resumes/', glob=f_doc_name)
    docs = loader.load()
    docs = docs[0]
    return(docs)

def get_pdf_data(doc_name): #Function which loads PDF files (Along with page numbers)
    f_doc_name = 'C:/Users/sbhadwal/SpecChat/Resumes/' + doc_name
    loader = PagedPDFSplitter(f_doc_name)
    pages = loader.load_and_split()
    return(pages)

sources = [                      #List of all the sources to be used
    get_pdf_data("software.pdf"),
    get_pdf_data("Kirthi_Nagane.pdf"),
    get_pdf_data("Vidhyasimhan_J_Resume.pdf"),
    get_pdf_data("Sujeet Neema - Cognitive Developer.pdf")
]

""" 
# Debugging, ignore #

sources = [get_pdf_data("Sujeet Neema - Cognitive Developer.pdf")]

sources = [get_pdf_data("Kirthi_Nagane.pdf")]

sources = [get_text_data("test")]

sources = [get_pdf_data("Vidhyasimhan_J_Resume.pdf")]

sources = [get_text_data("Sujeet Neema - Cognitive Developer")]
 """

source_chunks = []  #Creating chunks of the source documents    
splitter = CharacterTextSplitter(separator=" ", chunk_size=1024, chunk_overlap=0)
for source1 in sources: #For each of the source mentioned
    for source in source1: #Go to each page
        for chunk in splitter.split_text(source.page_content): #Chunk up the content in each page
            chunk = chunk + "Filename: " + source.metadata['source']
            source_chunks.append(Document(page_content=chunk, metadata=source.metadata))#Append it to source_chunks

search_index = FAISS.from_documents(source_chunks, HuggingFaceEmbeddings())   #Simiarity Search with HuggingFaceEmbeddings

template = """You are a chatbot having a conversation with a human.

Given the following extracted parts of a long document and a question, create a final answer.
Use only the information available in the context. Don't make up an answer.
Do not modify contact details. 
{context}

{chat_history}
Human: {human_input}
Chatbot:"""

prompt = PromptTemplate(
    input_variables=["chat_history", "human_input", "context"], 
    template=template
)

memory = ConversationBufferMemory(memory_key="chat_history", input_key="human_input")

chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff", prompt = prompt, memory=memory) #Lang chain 

def print_answer(question):
    print(
        chain(
            {
                "input_documents": search_index.similarity_search(question, k=4),
                "human_input": question,
            },
            return_only_outputs=False,   #Make it false if you want to see all that's being fed to ChatGPT (the imput docs and question)
        )
    )
    
#Test it out
print_answer("Who would be suitable for the role of Cloud Engineer")

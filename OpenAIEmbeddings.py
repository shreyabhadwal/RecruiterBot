from langchain.vectorstores import Chroma
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain import OpenAI, VectorDBQA
from langchain.document_loaders import PagedPDFSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains.llm import LLMChain
from langchain.chains.chat_vector_db.prompts import (CONDENSE_QUESTION_PROMPT, QA_PROMPT)
from langchain.prompts import PromptTemplate
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chains.question_answering import load_qa_chain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.chains import ChatVectorDBChain
import os

os.environ["OPENAI_API_KEY"] = "" #OpenAI Key
resume_path = 'C:/Users/sbhadwal/SpecChat/Resumes/Resumes_PDFs/'
sources = []

def get_pdf_data(doc_name): #Function which loads PDF files(Along with page numbers)
    f_doc_name = 'C:/Users/sbhadwal/SpecChat/Resumes/Resumes_PDFs/' + doc_name
    loader = PagedPDFSplitter(f_doc_name)
    pages = loader.load_and_split()
    return(pages)

dir_list = os.listdir(resume_path)

for i in dir_list:
    sources.append(get_pdf_data(i))

""" sources = [                      #List of all the sources to be used
    get_pdf_data("software.pdf"),
    get_pdf_data("Kirthi_Nagane.pdf"),
    get_pdf_data("Vidhyasimhan_J_Resume.pdf"),
    get_pdf_data("Sujeet Neema - Cognitive Developer.pdf")
]
 """
source_chunks = []  #Creating chunks of the source documents    
splitter = CharacterTextSplitter(separator=" ", chunk_size=1024, chunk_overlap=0)
for source1 in sources: #For each of the source mentioned
    for source in source1: #Go to each page
        for chunk in splitter.split_text(source.page_content): #Chunk up the content in each page
            chunk = chunk + "Filename is " + source.metadata['source']
            source_chunks.append(Document(page_content=chunk, metadata=source.metadata))#Append it to source_chunks

embeddings = OpenAIEmbeddings()
docsearch = FAISS.from_documents(source_chunks, embeddings)
#docsearch = Chroma.from_documents(source_chunks, embeddings) [IGNORE]

llm_gen = OpenAI(temperature=0,verbose=True) #Instantiate an LLM 
#llm_gen = OpenAI(model_name='gpt-3.5-turbo',temperature=0,verbose=True) #Instantiate an LLM 

question_generator = LLMChain(llm=llm_gen, prompt=CONDENSE_QUESTION_PROMPT) 
"""
Langchain to generate new question
(
The prompt template is: 
"Given the following conversation and a follow up question, 
rephrase the follow up question to be a standalone question.

Chat History:
{chat_history}

Follow Up Input: {question}

Standalone question:
"
)
"""


doc_chain = load_qa_chain(llm_gen, chain_type="stuff", prompt=QA_PROMPT)

"""
Langchain to make the final answer (from the top 4 chunks)
(
The prompt template is:
"Use the following pieces of context to answer the question at the end. 
If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question} 
Helpful Answer:"

)

Note: The question here is the new question that is created earlier from the (user question + chat histroy)
"""
qa = ChatVectorDBChain(                                 
    vectorstore=docsearch,
    combine_docs_chain=doc_chain,
    question_generator=question_generator,
    )

"""
Discovered ChatVectorDBChain (another langchain) while going through Langchain's Github. Helps us do exactly what we want. 
I had written a function for this process, but I feel doing it this way is faster and gives better results.

"""

chat_history = [] #Maintain a list for recording the chat history

def print_answer(question): 
    global chat_history
    result = qa(  #Run the chain
        {"question": question, "chat_history": chat_history},
        return_only_outputs=False,
        )
    chat_history.append((question, result["answer"])) #Update the chat history with the question asked and the answer
    print(result)

    if len(chat_history)>=5:
        chat_history=chat_history[1:]

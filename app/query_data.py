from langchain.callbacks.base import AsyncCallbackManager
from langchain.chains.chat_vector_db.prompts import (CONDENSE_QUESTION_PROMPT)
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.llm import LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores.base import VectorStore
from langchain.prompts import PromptTemplate

def get_chain(vectorstore: VectorStore, question_handler, stream_handler):

    manager = AsyncCallbackManager([])
    question_manager = AsyncCallbackManager([question_handler])
    stream_manager = AsyncCallbackManager([stream_handler])

    recruit_template  = """You are Hire Smith, a helpful AI assistant for job recruiters. Given the following pieces of context from a single or multiple resumes, answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

    {context}

    Question: {question}
    Helpful Answer:
    """

    recruit_prompt = PromptTemplate(template=recruit_template, input_variables=["context", "question"])

    question_gen_llm = OpenAI(
        temperature=0,
        verbose=True,
        callback_manager=question_manager,
        request_timeout=60,
        max_retries = 0
    )

    streaming_llm = OpenAI(
        streaming=True,
        callback_manager=stream_manager,
        verbose=True,
        temperature=0,
        request_timeout=60,
        max_retries = 0
    )

    question_generator = LLMChain(
        llm=question_gen_llm, prompt=CONDENSE_QUESTION_PROMPT, callback_manager=manager
    )

    doc_chain = load_qa_chain(
        streaming_llm, chain_type="stuff", prompt=recruit_prompt, callback_manager=manager
    )

    qa  = ConversationalRetrievalChain(
        retriever=vectorstore.as_retriever(),
        combine_docs_chain=doc_chain,
        question_generator=question_generator,
        callback_manager=manager,
    )

    return qa
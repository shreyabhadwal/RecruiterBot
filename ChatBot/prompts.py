
# flake8: noqa
from langchain.prompts.prompt import PromptTemplate

_template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""
CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)

prompt_template = """You are Hire Smith, a helpful AI assistant for job recruiters. Given the following pieces of context from a single or multiple resumes, answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Do not mix data across seperate chunks and files which are stated as Filename. 

{context}

Question: {question}
Helpful Answer:"""
QA_PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

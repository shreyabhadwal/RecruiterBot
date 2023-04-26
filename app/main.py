import logging
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from langchain.vectorstores import VectorStore
from callback import QuestionGenCallbackHandler, StreamingLLMCallbackHandler
from query_data import get_chain
from schemas import ChatResponse
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
import os


app = FastAPI()
app.mount("/templates", StaticFiles(directory="./templates"), name="templates")
templates = Jinja2Templates(directory="./templates")

vectorstore: Optional[VectorStore] = None
logger = logging.getLogger()
os.environ["OPENAI_API_KEY"] = "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" #OpenAI Key

@app.on_event("startup")
async def startup_event():
    global vectorstore
    vectorstore = FAISS.load_local("faiss_index", OpenAIEmbeddings())

@app.get("/")
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

#@app.websocket("/chat/")
@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()
    question_handler = QuestionGenCallbackHandler(websocket)
    stream_handler = StreamingLLMCallbackHandler(websocket)
    chat_history = []
    qa_chain = get_chain(vectorstore, question_handler, stream_handler)

    while True:
        try:
            # Receive and send back the client message
            question = await websocket.receive_text()
            resp = ChatResponse(sender="you", message=question, type="stream")
            #logging.info("resp: "+ str(resp.dict()))
            await websocket.send_json(resp.dict())
            #logging.info("resp: "+ resp.dict())

            # Construct a response
            start_resp = ChatResponse(sender="bot", message="", type="start")
            #logging.info("start_resp: "+ str(start_resp.dict()))
            await websocket.send_json(start_resp.dict())
            #logging.info("start_resp: "+ start_resp.dict())

            result = await qa_chain.acall(
                {"question": question, "chat_history": chat_history}
            )
            chat_history.append((question, result["answer"]))

            if len(chat_history)>=5:
                chat_history=chat_history[1:]

            end_resp = ChatResponse(sender="bot", message="", type="end")
            #logging.info("end_resp: "+ str(end_resp.dict()))
            await websocket.send_json(end_resp.dict())

        except WebSocketDisconnect:
            logging.info("websocket disconnect")
            break
             
        except Exception as e:
            logging.error(e)
            resp = ChatResponse(
                sender="bot",
                message="Sorry, something went wrong. Try again.",
                type="error",
            )
            await websocket.send_json(resp.dict())


if __name__ == "__main__":
    import uvicorn

    #uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 80)))
    uvicorn.run(app, host="0.0.0.0", port=8080)

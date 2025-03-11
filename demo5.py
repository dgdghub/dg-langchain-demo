# 抓数据，加载，分割，存储，检索，生成
import os

from bs4 import SoupStrainer
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain_chroma import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import Config

# 加载环境变量
cf = Config()
os.environ["LANGCHAIN_PROJECT"] = "demo4"  # 设置Langchain项目名称

# 创建聊天机器人
model_chat = ChatOpenAI(model=cf.OPENAI_MODEL)  # 使用OpenAI的GPT-4模型创建聊天机器人

# 1. 抓数据
loader = WebBaseLoader(
    # proxies={
    #     "http": os.getenv('http_proxy'),
    #     "https": os.getenv('https_proxy')
    # },
    web_path=
    [
        "https://www.cnn.com/2025/03/10/us/mahmoud-khalil-columbia-university-israel-hnk/index.html"
    ],
    bs_kwargs=dict(parse_only=SoupStrainer(
        class_=("headline__wrapper",
                "headline__text inline-placeholder vossi-headline-text",
                "headline__footer","headline__sub-container",
                "article__content-container"))),
)
# 加载数据
html = loader.load()
print(len(html))
print(html)

# 2. 分割数据
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# resp = splitter.split_text("hello, abcdef good moringing,fliter how are you doing, somhthing , usefull, 1234567890,how about you,im fine,thank you,goodbye")
# for str in resp:
#     print(str)
split_r = splitter.split_documents(html)

# 3. 存储数据
vector_store = Chroma.from_documents(documents=split_r, embedding=OpenAIEmbeddings())

# 4. 检索数据
retriever = vector_store.as_retriever()

# 5. 和大模型整合
system_prompt = """
You are an assistant for question-answering tasks. 
Use the following pieces of retrieved context to answer the question. 
If you don't know the answer, say that you don't know. Use three sentences maximum and keep the answer concise.\n
{context}
"""

prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder('chat_history'),
        ("human", "{input}")

    ]
)

# 6. 创建链
chain1 = create_stuff_documents_chain(model_chat, prompt_template)

# chain2 = create_retrieval_chain(retriever, chain1)

# 7 调用链
# resp = chain2.invoke({'input':'这篇新闻讲的什么？'})
# print(resp['answer'])

# 8. 子链
contextualize_q_template = """
Given a chat history and the latest user question
which might referene context in the chat history,
formulate a standalone question which can be understood without the chat history. Do NOT answer the question, just reformulate it if needed and otherwise return it as is.
"""

retriever_history_template = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_template),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}")
    ]
)


history_chain = create_history_aware_retriever(model_chat, retriever, retriever_history_template)

# 保存问答历史记录
history = {}
def get_session_history(session_id: str):
    if session_id not in history:
        history[session_id] = ChatMessageHistory()
    return history[session_id]

# 创建父链

chain = create_retrieval_chain(history_chain, chain1)
result_chain = RunnableWithMessageHistory(
    chain, get_session_history,
    input_messages_key='input',
    history_messages_key='chat_history',
    output_messages_key='answer'
)

resp1 = result_chain.invoke(
    {'input':'这篇新闻讲的什么？'},
    config={'configurable':{'session_id':'z1123'}}
)
print(resp1['answer'])

resp2 = result_chain.invoke(
    {'input':'这个新闻是谁发布的，什么时间发布的？'},
    config={'configurable':{'session_id':'z1123'}}
)
print(resp2['answer'])
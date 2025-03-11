# 通过上下文回答问题
import asyncio
import os

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from config import Config

# 加载环境变量
cf = Config()
os.environ["LANGCHAIN_PROJECT"] = "demo3"  # 设置Langchain项目名称

# 创建聊天机器人
model_chat = ChatOpenAI(model=cf.OPENAI_MODEL)  # 使用OpenAI的GPT-4模型创建聊天机器人

documents = [
    Document(
        page_content="猫是一种常见的家养宠物，以其独立和温柔的性格著称。",
        metadata={"type": "动物", "category": "哺乳动物", "description": "家猫"}
    ),
    Document(
        page_content="狗是非常忠诚的家养宠物，常被用作看门犬或导盲犬。",
        metadata={"type": "动物", "category": "哺乳动物", "description": "家狗"}
    ),
    Document(
        page_content="金鱼是最受欢迎的观赏鱼之一，以其鲜艳的颜色和简单的护理需求著称。",
        metadata={"type": "鱼类", "category": "淡水鱼", "description": "金鱼"}
    ),
    Document(
        page_content="鲨鱼是海洋中的顶级掠食者，以其强大的力量和独特的外观闻名。",
        metadata={"type": "鱼类", "category": "海水鱼", "description": "鲨鱼"}
    ),
    Document(
        page_content="鹦鹉是一种聪明的鸟类，以其模仿人类说话的能力而闻名。",
        metadata={"type": "动物", "category": "鸟类", "description": "鹦鹉"}
    ),
    Document(
        page_content="鲤鱼是中国传统节日中常见的观赏鱼，象征着好运和繁荣。",
        metadata={"type": "鱼类", "category": "淡水鱼", "description": "鲤鱼"}
    ),
    Document(
        page_content="大象是陆地上最大的哺乳动物，以其长鼻子和智慧著称。",
        metadata={"type": "动物", "category": "哺乳动物", "description": "大象"}
    ),
    Document(
        page_content="鲑鱼是一种洄游鱼类，每年都会从海洋游回河流产卵。",
        metadata={"type": "鱼类", "category": "海水鱼", "description": "鲑鱼"}
    ),
    Document(
        page_content="猴子是灵长类动物，以其灵活的身体和聪明的头脑著称。",
        metadata={"type": "动物", "category": "哺乳动物", "description": "猴子"}
    ),
    Document(
        page_content="热带鱼以其五彩斑斓的颜色和独特的形状而受到人们的喜爱。",
        metadata={"type": "鱼类", "category": "淡水鱼", "description": "热带鱼"}
    ),
    Document(
        page_content="宠物狗以其五活泼可爱，聪明听话而受到人们的喜爱。",
        metadata={"type": "狗类", "category": "宠物", "description": "家狗"}
    )
]

vector_store = Chroma.from_documents(documents, embedding = OpenAIEmbeddings())  # 创建Chroma对象
# print(vector_store.asimilarity_search_with_score("加菲猫"))

retriever = RunnableLambda(vector_store.asimilarity_search).bind(k=1)

message = '''
使用提供的上下文回答这个问题：
{question}
上下文：
{context}
'''

prompt_template = ChatPromptTemplate.from_messages([('human', message)])

chain = {'question': RunnablePassthrough(), 'context': retriever} | prompt_template | model_chat

async def main():
    resp = await chain.ainvoke('请介绍一下猫和狗?')
    print(resp.content)

asyncio.run(main())
import os  # 导入os模块，用于操作环境变量和文件路径

from fastapi import FastAPI  # 导入FastAPI，用于创建Web API服务
from langchain_core.output_parsers import StrOutputParser  # 导入StrOutputParser，用于将模型输出解析为字符串
from langchain_core.prompts import ChatPromptTemplate  # 导入ChatPromptTemplate，用于创建聊天提示模板
from langchain_openai import ChatOpenAI  # 导入ChatOpenAI，用于创建OpenAI的聊天模型
from langserve import add_routes  # 导入add_routes，用于将聊天链添加到FastAPI应用中

from config import Config
cf = Config()
# 创建模型
model_llm = ChatOpenAI(model = cf.OPENAI_MODEL)  # 使用OpenAI的GPT-4模型创建聊天模型

# 创建输出解析器
parser = StrOutputParser()  # 创建StrOutputParser实例，用于将模型输出解析为字符串

# 创建聊天模板
prompt_template = ChatPromptTemplate.from_messages([
    ('system', '请将以下内容翻译成{language}'),  # 系统消息模板，定义翻译任务
    ('user', '{text}')  # 用户消息模板，定义需要翻译的文本
])

# 创建聊天链
chain = prompt_template | model_llm | parser  # 将提示模板、聊天模型和输出解析器组合成聊天链

# 调用聊天链并打印结果
print(chain.invoke({'language': '英文', 'text': '我下午去不了，有一节课?'}))  # 调用聊天链，翻译文本并打印结果

# 创建FastAPI应用
app = FastAPI(title="Langchain Demo", version="0.1.0", description="Langchain Demo desc")  # 创建FastAPI应用实例

# 将聊天链添加到FastAPI应用中
add_routes(app,
           chain,
           path="/chat",  # 设置聊天链的访问路径
           )

# 启动FastAPI应用
if __name__ == "__main__":
    import uvicorn  # 导入uvicorn，用于启动FastAPI应用
    uvicorn.run(app, host="localhost", port=8000)  # 启动应用，监听localhost的8000端口
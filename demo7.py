# 抓数据，加载，分割，存储，检索，生成
import datetime
import os
from langchain_community.document_loaders import YoutubeLoader
from langchain_openai import ChatOpenAI

from config import Config

# 加载环境变量
cf = Config()
os.environ["LANGCHAIN_PROJECT"] = "demo7"  # 设置Langchain项目名称

# 创建聊天机器人
model_chat = ChatOpenAI(model=cf.OPENAI_MODEL)  # 使用OpenAI的GPT-4模型创建聊天机器人

persist_dir = 'chroma_data_dir'

urls = [
    "https://www.youtube.com/watch?v=HAn9vnJy6S4",
    "https://www.youtube.com/watch?v=dA1cHGACXCo",
    "https://www.youtube.com/watch?v=ZcEMLz27sL4",
    "https://www.youtube.com/watch?v=hvAPnpSfSGo",
    "https://www.youtube.com/watch?v=EhlPDL4QrWY",
    "https://www.youtube.com/watch?v=mmBo8nlu2j0",
    "https://www.youtube.com/watch?v=rQdib0sL1ps"
]

docs = []
for url in urls:
    docs.extend(YoutubeLoader.from_youtube_url(url, add_video_info=True).load())

print(len(docs))
print(docs[0])

for doc in docs:
    doc.metadata['publish_year'] = int(datetime.datetime.strptime(doc.metadata['publish_data'],'%Y-%m-%d %H:%M:%S').strptime('%Y'))

print(docs[0].metadata)
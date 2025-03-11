# 抓数据，加载，分割，存储，检索，生成
import os
import urllib

from langchain_community.utilities.sql_database import SQLDatabase
from langchain_openai import ChatOpenAI

from config import Config

# 加载环境变量
cf = Config()
os.environ["LANGCHAIN_PROJECT"] = "demo5"  # 设置Langchain项目名称

# 创建聊天机器人
model_chat = ChatOpenAI(model=cf.OPENAI_MODEL)  # 使用OpenAI的GPT-4模型创建聊天机器人
# 密码中包含了@，所以需要使用urllib.parse.quote_plus进行转义
url = f"mysql+pymysql://{cf.DB_USER}:{urllib.parse.quote_plus(cf.DB_PASSWORD)}@[{cf.DB_HOST}]:{cf.DB_PORT}/{cf.DB_NAME}"

print(url)
db = SQLDatabase.from_uri(url)  # 创建数据库连接

print(db.get_usable_table_names())
print(db.run("select * from t_user limit 10;"))
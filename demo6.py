# 抓数据，加载，分割，存储，检索，生成
import os
import urllib
from operator import itemgetter

from langchain.chains.sql_database.query import create_sql_query_chain
from langchain_community.tools import QuerySQLDatabaseTool
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

from config import Config

# 加载环境变量
cf = Config()
os.environ["LANGCHAIN_PROJECT"] = "demo6"  # 设置Langchain项目名称

# 创建聊天机器人
model_chat = ChatOpenAI(model=cf.OPENAI_MODEL)  # 使用OpenAI的GPT-4模型创建聊天机器人
# 密码中包含了@，所以需要使用urllib.parse.quote_plus进行转义
url = f"mysql+pymysql://{cf.DB_USER}:{urllib.parse.quote_plus(cf.DB_PASSWORD)}@[{cf.DB_HOST}]:{cf.DB_PORT}/{cf.DB_NAME}"

# print(url)
db = SQLDatabase.from_uri(url)  # 创建数据库连接

# print(db.get_usable_table_names())
# print(db.run("select * from t_user limit 10;"))

db_chain = create_sql_query_chain(model_chat, db)  # 创建查询链
resp = db_chain.invoke({"question": "有几个用户"})  # 查询数据库
print(resp)

# 创建提示词模版
answer_prompt = PromptTemplate.from_template(
    """
    给定以下用户问题、Sql语句和Sql执行后的结果，回答用户问题
    Question: {question}
    SQL Query: {query}
    SQL Result: {result}
    回答: 
    """
)

exec_sql = QuerySQLDatabaseTool(db=db)  # 创建查询工具
# 创建查询链, 链的连接过程中，需要注意次序，例如prompt在model前面，因为prompt需要model的输出
query_chain = (RunnablePassthrough.assign(query=db_chain).assign(result = itemgetter('query') | exec_sql)
                 | answer_prompt
                 | model_chat
                 | StrOutputParser()
)

resp = query_chain.invoke(input={"question": "有几个用户"})
print(resp)
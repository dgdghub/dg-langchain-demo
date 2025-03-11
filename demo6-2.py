# 抓数据，加载，分割，存储，检索，生成
import os
import urllib

from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import chat_agent_executor

from config import Config

# 加载环境变量
cf = Config()
os.environ["LANGCHAIN_PROJECT"] = "demo5"  # 设置Langchain项目名称

# 创建聊天机器人
model_chat = ChatOpenAI(model=cf.OPENAI_MODEL)  # 使用OpenAI的GPT-4模型创建聊天机器人
# 密码中包含了@，所以需要使用urllib.parse.quote_plus进行转义
url = f"mysql+pymysql://{cf.DB_USER}:{urllib.parse.quote_plus(cf.DB_PASSWORD)}@[{cf.DB_HOST}]:{cf.DB_PORT}/{cf.DB_NAME}"

# print(url)
db = SQLDatabase.from_uri(url)  # 创建数据库连接

# 创建工具
tool_kits = SQLDatabaseToolkit(db = db, llm = model_chat)
tools = tool_kits.get_tools()

# 创建提示模版
system_prompt = """
您是一个被设计用来与SQL数据库交互的代理。
给定一个输入问题，创建一个语法正确的SQL语句并执行，然后查看查询结果并返回答案。
除非用户指定了他们想要获得的示例的具体数量，否则始终将SQL查询限制为最多10个结果。
你可以按相关列对结果进行排序，以返回MySQL数据库中最匹配的数据。
您可以使用与数据库交互的工具。在执行查询之前，你必须仔细检查。如果在执行查询时出现错误，请重写查询并重试。
不要对数据库做任何DML语句（插入，更新，删除，删除等）。
首先，你应该查看数据库中的表，看看可以查询什么。
不要跳过这一步。
然后查询最相关的表的模式。
"""

system_message = SystemMessage(content=system_prompt)
# 创建代理

agent_sql = chat_agent_executor.create_tool_calling_executor(model_chat, tools, system_message)

resp = agent_sql.invoke({"messages": [HumanMessage(content="有多少用户")]})
result = resp['messages']
print(len(result))
print(result)

print(result[len(result)-1])
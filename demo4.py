# 使用tavily 搜索工具，使用agent_executor工具
import os

from langchain_community.tools import TavilySearchResults
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import chat_agent_executor

from config import Config

# 加载环境变量
cf = Config()
os.environ["LANGCHAIN_PROJECT"] = "demo4"  # 设置Langchain项目名称

# 创建聊天机器人
model_chat = ChatOpenAI(model=cf.OPENAI_MODEL)  # 使用OpenAI的GPT-4模型创建聊天机器人

# result = model_chat.invoke([HumanMessage(content="上海今天天气怎么样?")])  # 调用聊天机器人，发送消息并获取结果
#
# print(result)

search = TavilySearchResults(max_results=2)
# print(search.invoke("上海今天天气怎么样?"))
# # 模型绑定工具
# model_with_tool  = model_chat.bind_tools([search])
#
# resp = model_with_tool.invoke([HumanMessage(content="美国的首都是哪里?")])
# print(f'Model_result_content: {resp.content}')
# print(f'Tool_result_content: {resp.tool_calls}')
#
# resp2 = model_with_tool.invoke([HumanMessage(content="上海今天天气怎么样?")])
# print(f'Model_result_content: {resp2.content}')
# print(f'Tool_result_content: {resp2.tool_calls}')

tools = [search]

agent_executor = chat_agent_executor.create_tool_calling_executor(model_chat, tools)
resp1 = agent_executor.invoke({'messages':[HumanMessage(content="美国的首都是哪里?")]})
print(resp1['messages'])

resp2 = agent_executor.invoke({'messages':[HumanMessage(content="上海今天天气怎么样?")]})
print(resp2['messages'])

print(resp2['messages'][2].content)
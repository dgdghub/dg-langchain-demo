import os

from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

from config import Config
# 加载环境变量
cf = Config()

os.environ["LANGCHAIN_PROJECT"] = "demo2"
# 创建聊天机器人
model_chat = ChatOpenAI(model=cf.OPENAI_MODEL)

# 定义模版
prompt_template = ChatPromptTemplate.from_messages([
    ('system', '你是一个专业助手，请用{language}尽所能回答所有问题。'),
    MessagesPlaceholder(variable_name='my_msg')
])

# 创建聊天链
chain = prompt_template | model_chat

history_msgs = {}
# 获取聊天历史
def get_history_msg(session_id: str):
    if session_id not in history_msgs:
        history_msgs[session_id] = ChatMessageHistory()

    return history_msgs[session_id]

do_msg = RunnableWithMessageHistory(
    chain,
    get_history_msg,
    input_messages_key='my_msg'
)

config = {
    'configurable': {'session_id': 'dp123'}
}
# 第一轮
resp1 = do_msg.invoke(
    { 'language': '中文',
      'my_msg': [HumanMessage(content='你好，我是dp')],
    },
    config=config
)

print(resp1.content)

# 第二轮
resp2 = do_msg.invoke(
    { 'language': '中文',
      'my_msg': [HumanMessage(content='请问，我的名字叫什么?')],
    },
    config=config
)

print(resp2.content)

# 第三轮, 流式输出
config = {
    'configurable': {'session_id': 'dp1234'}
}
for resp in do_msg.stream({ 'language': '英文','my_msg': [HumanMessage(content='你有什么功能?')]},config=config):
    print(resp.content, end=' - ')

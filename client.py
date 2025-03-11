# 调用fastapi服务
from langserve import RemoteRunnable

if __name__ == '__main__':
    client = RemoteRunnable('http://localhost:8000/chat')
    print(client.invoke({"language": "法语", "text": "我下午去不了，有一节课?"}))
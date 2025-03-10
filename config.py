
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_MODEL = os.getenv('OPENAI_MODEL')
    def __init__(self):
        # 设置OpenAI的API环境变量
        os.environ['OPENAI_API_BASE'] = os.getenv('OPENAI_API_BASE')
        os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

        # 设置代理
        os.environ['http_proxy'] = os.getenv('http_proxy')
        os.environ['https_proxy'] = os.getenv('https_proxy')

        # 设置环境变量
        os.environ["LANGCHAIN_TRACING_V2"] = os.getenv('LANGCHAIN_TRACING_V2')
        os.environ["LANGCHAIN_PROJECT"] = os.getenv('LANGCHAIN_PROJECT')
        os.environ["LANGCHAIN_API_KEY"] = os.getenv('LANGCHAIN_API_KEY')
        os.environ["TAVILY_API_KEY"] = os.getenv('TAVILY_API_KEY')

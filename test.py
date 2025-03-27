# 修复SSL配置
import ssl
from urllib.request import urlopen
import certifi

def create_custom_ssl_context():
    """创建携带certifi证书的SSL上下文"""
    return ssl.create_default_context(cafile=certifi.where())

# 关键修复：将函数引用赋给上下文生成器
ssl._create_default_https_context = create_custom_ssl_context

# 验证配置是否生效
try:
    response = urlopen("https://www.youtube.com")
    print("SSL验证成功！状态码:", response.status)
except Exception as e:
    print("验证失败:", str(e))
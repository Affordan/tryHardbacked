import uvicorn
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

if __name__ == "__main__":
    # 启动 FastAPI 应用服务器
    # host: 服务器监听的主机地址，127.0.0.1 表示只允许本地访问
    # port: 服务器监听的端口号
    # reload: 开发模式，代码变更时自动重载服务器
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
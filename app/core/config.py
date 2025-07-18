import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# Dify AI API 配置 (向后兼容，用于原始对话功能)
DIFY_API_URL = os.getenv("DIFY_API_URL", "https://api.dify.ai/v1/chat-messages")
DIFY_API_KEY = os.getenv("DIFY_API_KEY", "")

# Dify Workflow API 配置 (统一工作流端点)
# 所有Dify工作流使用统一的API端点
DIFY_WORKFLOW_API_URL = os.getenv("DIFY_WORKFLOW_API_URL", "https://api.dify.ai/v1/workflows/run")

# 查询并回答工作流API密钥
DIFY_QNA_WORKFLOW_API_KEY = os.getenv("DIFY_QNA_WORKFLOW_API_KEY", "")

# 简述自己的身世工作流API密钥
DIFY_MONOLOGUE_WORKFLOW_API_KEY = os.getenv("DIFY_MONOLOGUE_WORKFLOW_API_KEY", "")

# LangChain 配置
# LangSmith API key for tracing (optional)
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY", "")
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "murder-mystery-game")

# Game Engine 配置
# Maximum number of Q&A rounds per character per act
MAX_QNA_PER_CHARACTER_PER_ACT = int(os.getenv("MAX_QNA_PER_CHARACTER_PER_ACT", "3"))
# Maximum number of acts in a game
MAX_ACTS = int(os.getenv("MAX_ACTS", "3"))
# Game session timeout in minutes
GAME_SESSION_TIMEOUT_MINUTES = int(os.getenv("GAME_SESSION_TIMEOUT_MINUTES", "120"))

# 数据库配置
# SQLite 数据库连接字符串，数据库文件存储在项目根目录
DATABASE_URL = "sqlite:///./game_database.db"
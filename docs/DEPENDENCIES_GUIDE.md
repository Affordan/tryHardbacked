# 依赖配置指南

## 📦 requirements.txt 配置说明

本文档详细说明了谋杀悬疑游戏后端系统的依赖配置，基于实际代码分析和项目需求优化。

## 🏗️ 依赖分类

### 1. 核心 Web 框架依赖

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
```

**说明**：
- `fastapi==0.104.1`: 现代、快速的 Web 框架，支持自动 API 文档生成
- `uvicorn[standard]==0.24.0`: ASGI 服务器，包含标准扩展（WebSocket、HTTP/2 支持）

**使用位置**：
- `app/main.py`: FastAPI 应用入口
- `app/routers/*.py`: 所有 API 路由模块

### 2. 数据库和数据验证

```txt
sqlalchemy==2.0.23
pydantic==2.5.0
```

**说明**：
- `sqlalchemy==2.0.23`: ORM 框架，用于数据库操作
- `pydantic==2.5.0`: 数据验证和序列化框架

**使用位置**：
- `app/models/database_models.py`: SQLAlchemy 数据模型
- `app/schemas/pydantic_schemas.py`: API 数据验证模式
- `app/langchain/state/models.py`: 游戏状态 Pydantic 模型

### 3. HTTP 客户端和安全

```txt
requests==2.31.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
```

**说明**：
- `requests==2.31.0`: HTTP 客户端，用于调用 Dify API
- `python-jose[cryptography]==3.3.0`: JWT 令牌处理（预留功能）
- `passlib[bcrypt]==1.7.4`: 密码哈希处理（预留功能）

**使用位置**：
- `app/services/dify_service.py`: Dify API 调用

### 4. LangChain 游戏引擎核心依赖

```txt
langchain>=0.3.26
langchain-core>=0.3.68
langchain-community>=0.3.27
langgraph>=0.5.3
```

**说明**：
- `langchain>=0.3.26`: LangChain 主框架
- `langchain-core>=0.3.68`: LangChain 核心组件
- `langchain-community>=0.3.27`: 社区工具和集成
- `langgraph>=0.5.3`: 状态图编排框架

**使用位置**：
- `app/langchain/tools/dify_tools.py`: LangChain 自定义工具
- `app/langchain/engine/graph.py`: LangGraph 状态机
- `app/langchain/engine/game_engine.py`: 游戏引擎

### 5. 开发和测试依赖

```txt
pytest>=7.0.0
pytest-asyncio>=0.21.0
pytest-mock>=3.10.0
```

**说明**：
- `pytest>=7.0.0`: 测试框架
- `pytest-asyncio>=0.21.0`: 异步测试支持
- `pytest-mock>=3.10.0`: Mock 测试工具

**使用位置**：
- `tests/`: 所有测试文件

### 6. 代码质量工具（可选）

```txt
black>=23.0.0
flake8>=6.0.0
isort>=5.12.0
```

**说明**：
- `black>=23.0.0`: 代码格式化工具
- `flake8>=6.0.0`: 代码风格检查
- `isort>=5.12.0`: 导入语句排序

### 7. 生产环境依赖（可选）

```txt
python-dotenv>=1.0.0
```

**说明**：
- `python-dotenv>=1.0.0`: 环境变量管理

## 🚀 安装指南

### 1. 基础安装（最小依赖）

```bash
# 只安装核心运行依赖
pip install fastapi==0.104.1 uvicorn[standard]==0.24.0 sqlalchemy==2.0.23 pydantic==2.5.0 requests==2.31.0
```

### 2. 完整安装（推荐）

```bash
# 安装所有依赖
pip install -r requirements.txt
```

### 3. 分步安装（故障排除）

```bash
# 1. 核心框架
pip install fastapi==0.104.1 uvicorn[standard]==0.24.0

# 2. 数据层
pip install sqlalchemy==2.0.23 pydantic==2.5.0

# 3. HTTP 和安全
pip install requests==2.31.0 python-jose[cryptography]==3.3.0 passlib[bcrypt]==1.7.4

# 4. LangChain 组件
pip install langchain>=0.3.26 langchain-core>=0.3.68 langchain-community>=0.3.27 langgraph>=0.5.3

# 5. 测试工具
pip install pytest>=7.0.0 pytest-asyncio>=0.21.0 pytest-mock>=3.10.0

# 6. 开发工具（可选）
pip install black>=23.0.0 flake8>=6.0.0 isort>=5.12.0 python-dotenv>=1.0.0
```

## 🔧 版本兼容性

### Python 版本要求
- **最低要求**: Python 3.9+
- **推荐版本**: Python 3.10 或 3.11
- **测试版本**: Python 3.9, 3.10, 3.11

### 关键依赖版本说明

| 依赖 | 版本 | 说明 |
|------|------|------|
| FastAPI | 0.104.1 | 稳定版本，支持所有需要的功能 |
| Pydantic | 2.5.0 | V2 版本，性能更好，类型检查更严格 |
| SQLAlchemy | 2.0.23 | 2.0 版本，现代 ORM 特性 |
| LangChain | >=0.3.26 | 最新稳定版本，支持所有工具功能 |
| LangGraph | >=0.5.3 | 状态图功能完整版本 |

## 🐛 常见问题解决

### 1. LangChain 安装失败

```bash
# 问题：版本冲突
# 解决：升级 pip 和 setuptools
pip install --upgrade pip setuptools wheel
pip install langchain langgraph langchain-core langchain-community
```

### 2. cryptography 编译错误

```bash
# 问题：缺少编译工具
# Windows 解决方案：
pip install --only-binary=cryptography python-jose[cryptography]

# Linux 解决方案：
sudo apt-get install build-essential libffi-dev
pip install python-jose[cryptography]
```

### 3. SQLAlchemy 版本兼容性

```bash
# 问题：SQLAlchemy 1.x 和 2.x 不兼容
# 解决：确保使用 2.0+ 版本
pip install --upgrade sqlalchemy>=2.0.23
```

## 📋 依赖检查清单

### 安装后验证

```bash
# 检查关键依赖是否正确安装
python -c "import fastapi; print(f'FastAPI: {fastapi.__version__}')"
python -c "import langchain; print(f'LangChain: {langchain.__version__}')"
python -c "import langgraph; print(f'LangGraph: {langgraph.__version__}')"
python -c "import sqlalchemy; print(f'SQLAlchemy: {sqlalchemy.__version__}')"
python -c "import pydantic; print(f'Pydantic: {pydantic.__version__}')"
```

### 功能验证

```bash
# 启动应用验证
uvicorn app.main:app --reload --port 8000

# 访问 API 文档验证
curl http://localhost:8000/docs
```

## 🔄 更新策略

### 定期更新

```bash
# 检查过时的包
pip list --outdated

# 更新非关键依赖
pip install --upgrade black flake8 isort pytest

# 谨慎更新核心依赖（需要测试）
pip install --upgrade fastapi uvicorn sqlalchemy pydantic
```

### 锁定版本

对于生产环境，建议使用 `pip freeze` 生成精确版本：

```bash
pip freeze > requirements-lock.txt
```

## 📚 相关文档

- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [LangChain 官方文档](https://python.langchain.com/)
- [LangGraph 文档](https://langchain-ai.github.io/langgraph/)
- [Pydantic 文档](https://docs.pydantic.dev/)
- [SQLAlchemy 文档](https://docs.sqlalchemy.org/)

import requests
import time
import logging
from typing import Dict, Any, Optional
from enum import Enum
from app.core.config import (
    DIFY_API_URL, DIFY_API_KEY,  # 向后兼容
    DIFY_WORKFLOW_API_URL,
    DIFY_QNA_WORKFLOW_API_KEY,
    DIFY_MONOLOGUE_WORKFLOW_API_KEY
)
from app.schemas.pydantic_schemas import DialogueRequest

logger = logging.getLogger(__name__)


class DifyWorkflowType(str, Enum):
    """Enumeration of available Dify workflows."""
    QNA_WORKFLOW = "qna_workflow"  # 查询并回答 workflow
    MONOLOGUE_WORKFLOW = "monologue_workflow"  # 简述自己的身世 workflow


class DifyServiceError(Exception):
    """Custom exception for Dify service errors."""
    pass


def call_dify_chatflow(request: DialogueRequest, user_id: str, formatted_prompt: str = "") -> str:
    """
    调用 Dify AI 平台的聊天消息 API
    
    Args:
        request: 对话请求对象，包含会话ID和用户问题
        user_id: 用户唯一标识符
    
    Returns:
        str: AI 生成的回答文本
    """
    # 设置请求头，包含认证信息
    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",  # Bearer Token 认证
        "Content-Type": "application/json",  # JSON 格式请求
    }

    # 构建请求体，符合 Dify API 规范
    body = {
        "inputs": {},  # 输入参数（当前为空）
        "query": request.question,  # 用户的问题
        "user": user_id,  # 用户标识符
        "conversation_id": request.session_id,  # 会话ID，用于保持对话上下文
        "response_mode": "blocking"  # 阻塞模式，等待完整响应
    }
    
    try:
        # 发送 POST 请求到 Dify API
        response = requests.post(DIFY_API_URL, headers=headers, json=body)
        response.raise_for_status()  # 检查 HTTP 状态码，如有错误则抛出异常

        # 解析 JSON 响应
        api_response = response.json()
        # 返回 AI 的回答，如果没有答案则返回默认消息
        return api_response.get("answer", "抱歉，我暂时无法回答。")

    except requests.exceptions.RequestException as e:
        # 处理网络请求异常（连接超时、网络错误等）
        logger.error(f"调用 Dify API 时发生错误: {e}")
        return "AI 服务当前不可用，请稍后再试。"


def call_dify_workflow(
    workflow_type: DifyWorkflowType,
    inputs: Dict[str, Any],
    user_id: str,
    max_retries: int = 3,
    timeout: int = 30
) -> str:
    """
    调用 Dify 工作流 API (支持流式响应)

    Args:
        workflow_type: 工作流类型
        inputs: 输入参数字典
        user_id: 用户唯一标识符
        max_retries: 最大重试次数
        timeout: 请求超时时间（秒）

    Returns:
        str: 解析后的中文响应内容

    Raises:
        DifyServiceError: 当 API 调用失败时
    """
    # 根据工作流类型选择API密钥
    if workflow_type == DifyWorkflowType.QNA_WORKFLOW:
        api_key = DIFY_QNA_WORKFLOW_API_KEY
    elif workflow_type == DifyWorkflowType.MONOLOGUE_WORKFLOW:
        api_key = DIFY_MONOLOGUE_WORKFLOW_API_KEY
    else:
        raise DifyServiceError(f"Unsupported workflow type: {workflow_type}")

    if not api_key:
        raise DifyServiceError(f"API key not configured for workflow type: {workflow_type}")

    # Validate and sanitize user_id to prevent 400 errors
    if not user_id or not user_id.strip():
        user_id = "anonymous_user"
        logger.warning(f"Empty user_id provided, using fallback: {user_id}")

    # 设置请求头
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    # 构建请求体 - 使用流式响应
    body = {
        "inputs": inputs,
        "user": user_id.strip(),  # Ensure no leading/trailing whitespace
        "response_mode": "streaming"
    }

    last_exception = None

    # 重试逻辑
    for attempt in range(max_retries):
        try:
            logger.info(f"Calling Dify workflow {workflow_type}, attempt {attempt + 1}")

            # Debug logging - log the complete request details
            logger.info(f"Request URL: {DIFY_WORKFLOW_API_URL}")
            logger.info(f"Request headers: {headers}")
            logger.info(f"Request body: {body}")

            # 发送流式请求
            response = requests.post(
                DIFY_WORKFLOW_API_URL,
                headers=headers,
                json=body,
                timeout=timeout,
                stream=True
            )

            # Log response details for debugging
            logger.info(f"Response status code: {response.status_code}")
            logger.info(f"Response headers: {dict(response.headers)}")

            response.raise_for_status()

            # 设置UTF-8编码
            response.encoding = 'utf-8'

            # 解析流式响应
            result_content = _parse_streaming_response(response)

            logger.info(f"Successfully called Dify workflow {workflow_type}")
            return result_content

        except requests.exceptions.Timeout as e:
            last_exception = e
            logger.warning(f"Timeout on attempt {attempt + 1} for {workflow_type}: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff

        except requests.exceptions.RequestException as e:
            last_exception = e
            logger.error(f"Request error on attempt {attempt + 1} for {workflow_type}: {e}")

            # Log detailed error response if available
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Error response status: {e.response.status_code}")
                logger.error(f"Error response headers: {dict(e.response.headers)}")
                try:
                    error_body = e.response.text
                    logger.error(f"Error response body: {error_body}")
                except:
                    logger.error("Could not read error response body")

            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)

        except Exception as e:
            last_exception = e
            logger.error(f"Unexpected error on attempt {attempt + 1} for {workflow_type}: {e}")
            break  # Don't retry on unexpected errors

    # All retries failed
    raise DifyServiceError(f"Failed to call {workflow_type} after {max_retries} attempts: {last_exception}")


def call_qna_workflow(
    char_id: str,
    act_num: int,
    query: str,
    history: Optional[str],  # Add this parameter
    model_name: str,
    user_id: str
) -> str:
    """
    调用查询并回答工作流

    Args:
        char_id: 角色ID
        act_num: 幕数
        query: 查询问题
        model_name: 模型名称
        user_id: 用户ID
        history: 游戏历史上下文（可选）

    Returns:
        str: AI 生成的回答

    Raises:
        DifyServiceError: 当工作流调用失败时
    """
    # Validate required parameters to prevent 400 errors
    if not user_id or not user_id.strip():
        logger.warning("Empty user_id provided to call_qna_workflow")
        user_id = "anonymous_user"

    if not char_id or not char_id.strip():
        logger.warning("Empty char_id provided to call_qna_workflow")
        char_id = "unknown_character"

    # Truncate history to meet Dify API requirements (max 256 characters)
    processed_history = history or "没有历史记录。"
    if len(processed_history) > 256:
        # Smart truncation: try to keep the most recent and relevant information
        processed_history = _truncate_history_smartly(processed_history, char_id)
        logger.warning(f"History truncated from {len(history)} to {len(processed_history)} characters for Dify API")

    inputs = {
        "char_id": char_id.strip() if char_id else "unknown_character",
        "act_num": act_num,
        "query": query or "",  # Ensure query is never None
        "model_name": model_name or "gpt-3.5-turbo",  # Default model
        "history": processed_history  # Truncated history
    }

    try:
        # 直接返回流式响应解析的结果
        answer = call_dify_workflow(
            DifyWorkflowType.QNA_WORKFLOW,
            inputs,
            user_id
        )
        return answer

    except DifyServiceError as e:
        logger.error(f"QnA workflow failed: {e}")
        return "抱歉，我暂时无法回答这个问题。"


def call_monologue_workflow(
    char_id: str,
    act_num: int,
    model_name: str,
    user_id: str
) -> str:
    """
    调用简述自己的身世工作流

    Args:
        char_id: 角色ID
        act_num: 幕数
        model_name: 模型名称
        user_id: 用户ID

    Returns:
        str: AI 生成的角色独白

    Raises:
        DifyServiceError: 当工作流调用失败时
    """
    # Validate required parameters to prevent 400 errors
    if not user_id or not user_id.strip():
        logger.warning("Empty user_id provided to call_monologue_workflow")
        user_id = "anonymous_user"

    if not char_id or not char_id.strip():
        logger.warning("Empty char_id provided to call_monologue_workflow")
        char_id = "unknown_character"

    inputs = {
        "char_id": char_id.strip() if char_id else "unknown_character",
        "act_num": act_num,
        "model_name": model_name or "gpt-3.5-turbo"  # Default model
    }

    try:
        # 直接返回流式响应解析的结果
        monologue = call_dify_workflow(
            DifyWorkflowType.MONOLOGUE_WORKFLOW,
            inputs,
            user_id
        )
        return monologue

    except DifyServiceError as e:
        logger.error(f"Monologue workflow failed: {e}")
        return "抱歉，我暂时无法生成角色独白。"





def _truncate_history_smartly(history: str, char_id: str, max_length: int = 256) -> str:
    """
    智能截断历史记录，优先保留与当前角色相关的最新信息

    Args:
        history: 原始历史记录
        char_id: 当前角色ID
        max_length: 最大长度限制

    Returns:
        str: 截断后的历史记录
    """
    if len(history) <= max_length:
        return history

    # 保留一些空间给结尾标识符
    target_length = max_length - 10

    # 尝试按行分割，优先保留与当前角色相关的内容
    lines = history.split('\n')

    # 查找与当前角色相关的行
    relevant_lines = []
    other_lines = []

    for line in lines:
        if char_id in line:
            relevant_lines.append(line)
        else:
            other_lines.append(line)

    # 构建截断后的历史记录
    result_lines = []
    current_length = 0

    # 首先添加与当前角色相关的最新内容
    for line in reversed(relevant_lines):
        if current_length + len(line) + 1 <= target_length:  # +1 for newline
            result_lines.insert(0, line)
            current_length += len(line) + 1
        else:
            break

    # 如果还有空间，添加其他最新内容
    for line in reversed(other_lines):
        if current_length + len(line) + 1 <= target_length:
            result_lines.insert(0, line)
            current_length += len(line) + 1
        else:
            break

    # 如果仍然太长，进行简单截断
    result = '\n'.join(result_lines)
    if len(result) > target_length:
        result = result[:target_length]

    return result + "...(历史记录已截断)"


def _parse_streaming_response(response) -> str:
    """
    解析Dify流式响应，提取中文内容

    Args:
        response: requests响应对象

    Returns:
        str: 解析后的中文内容
    """
    import json

    result_parts = []

    try:
        # 遍历响应的每一行
        for line in response.iter_lines(decode_unicode=True):
            # SSE 事件通常以 "data: " 开头
            if line and line.startswith('data: '):
                # 移除 "data: " 前缀
                json_string = line[len('data: '):]

                # 流结束标记
                if json_string.strip() == '[DONE]':
                    break

                try:
                    # 解析JSON数据
                    data = json.loads(json_string)

                    # 提取文本内容
                    if 'event' in data and data['event'] == 'text_chunk':
                        if 'data' in data and 'text' in data['data']:
                            result_parts.append(data['data']['text'])
                    elif 'event' in data and data['event'] == 'workflow_finished':
                        # 工作流完成，可能包含最终结果
                        if 'data' in data and 'outputs' in data['data']:
                            outputs = data['data']['outputs']
                            # 尝试从outputs中提取结果
                            for key, value in outputs.items():
                                if isinstance(value, str) and value.strip():
                                    result_parts.append(value)

                except json.JSONDecodeError:
                    # 忽略无效的JSON行
                    continue

        # 合并所有文本片段
        result = ''.join(result_parts).strip()

        if not result:
            return "抱歉，未能获取到有效响应。"

        return result

    except Exception as e:
        logger.error(f"Failed to parse streaming response: {e}")
        return "抱歉，响应解析失败。"


def _extract_answer_from_response(response: Dict[str, Any]) -> str:
    """
    从工作流响应中提取答案 (兼容旧版本)

    Args:
        response: API 响应数据

    Returns:
        str: 提取的答案文本
    """
    try:
        # 尝试从不同可能的字段中提取答案
        data = response.get("data", {})
        outputs = data.get("outputs", {})

        # 常见的输出字段名
        possible_fields = ["answer", "result", "output", "text", "content"]

        for field in possible_fields:
            if field in outputs and outputs[field]:
                return str(outputs[field])

        # 如果没有找到标准字段，返回第一个非空值
        for key, value in outputs.items():
            if value and isinstance(value, (str, int, float)):
                return str(value)

        # 最后的备选方案
        return "抱歉，无法解析AI响应。"

    except Exception as e:
        logger.error(f"Failed to extract answer from response: {e}")
        return "抱歉，响应解析失败。"
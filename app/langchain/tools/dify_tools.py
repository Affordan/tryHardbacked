"""
LangChain custom tools for Dify workflow integration.

This module provides LangChain tools that wrap the Dify workflows as external AI services,
allowing the game engine to call specific AI functions for character interactions.
"""

import logging
from typing import Optional, Dict, Any, Type
from pydantic import BaseModel, Field, field_validator
from langchain_core.tools import BaseTool

from app.services.dify_service import call_monologue_workflow, call_qna_workflow, DifyServiceError

logger = logging.getLogger(__name__)


class MonologueInput(BaseModel):
    """Input schema for the monologue tool."""
    char_id: str = Field(..., description="Character ID for the monologue")
    act_num: int = Field(..., description="Act number (1-3)", ge=1, le=3)
    model_name: str = Field(default="gpt-3.5-turbo", description="AI model name to use")
    user_id: str = Field(..., description="User ID for the request")
    
    @field_validator('char_id')
    @classmethod
    def validate_char_id(cls, v):
        if not v or not v.strip():
            raise ValueError("Character ID cannot be empty")
        return v.strip()


class QnAInput(BaseModel):
    """Input schema for the Q&A tool."""
    char_id: str = Field(..., description="Character ID to ask the question to")
    act_num: int = Field(..., description="Act number (1-3)", ge=1, le=3)
    query: str = Field(..., description="Question to ask the character")
    model_name: str = Field(default="gpt-3.5-turbo", description="AI model name to use")
    user_id: str = Field(..., description="User ID for the request")
    
    @field_validator('char_id')
    @classmethod
    def validate_char_id(cls, v):
        if not v or not v.strip():
            raise ValueError("Character ID cannot be empty")
        return v.strip()

    @field_validator('query')
    @classmethod
    def validate_query(cls, v):
        if not v or not v.strip():
            raise ValueError("Query cannot be empty")
        if len(v.strip()) > 1000:
            raise ValueError("Query is too long (max 1000 characters)")
        return v.strip()


class DifyMonologueTool(BaseTool):
    """
    LangChain tool for generating character monologues using Dify workflow.

    This tool wraps the '简述自己的身世' Dify workflow, allowing characters
    to provide background information about themselves.
    """

    name: str = "dify_monologue"
    description: str = (
        "Generate a character monologue using Dify AI workflow. "
        "Use this tool when a character needs to introduce themselves or "
        "provide background information about their history and personality. "
        "Input should include char_id, act_num, model_name, and user_id."
    )
    return_direct: bool = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.args_schema = MonologueInput
    
    def _run(
        self,
        char_id: str,
        act_num: int,
        model_name: str,
        user_id: str,
    ) -> str:
        """
        Execute the monologue generation.
        
        Args:
            char_id: Character ID
            act_num: Act number
            model_name: AI model name
            user_id: User ID
            run_manager: Callback manager for tool execution
            
        Returns:
            Generated monologue text
        """
        try:
            logger.info(f"Generating monologue for character {char_id}, act {act_num}")

            # Call the Dify monologue workflow
            monologue = call_monologue_workflow(
                char_id=char_id,
                act_num=act_num,
                model_name=model_name,
                user_id=user_id
            )

            logger.info(f"Successfully generated monologue for character {char_id}")
            return monologue
            
        except DifyServiceError as e:
            error_msg = f"Dify service error for character {char_id}: {e}"
            logger.error(error_msg)
            return f"抱歉，{char_id}暂时无法进行自我介绍。请稍后再试。"

        except Exception as e:
            error_msg = f"Unexpected error generating monologue for character {char_id}: {e}"
            logger.error(error_msg)
            return f"抱歉，生成{char_id}的独白时发生了错误。"
    
    async def _arun(
        self,
        char_id: str,
        act_num: int,
        model_name: str,
        user_id: str,
    ) -> str:
        """Async version of the tool execution."""
        # For now, just call the sync version
        # In a production environment, you might want to implement true async calls
        return self._run(char_id, act_num, model_name, user_id)


class DifyQnATool(BaseTool):
    """
    LangChain tool for character Q&A using Dify workflow.

    This tool wraps the '查询并回答' Dify workflow, allowing players
    to ask questions to characters and receive AI-generated responses.
    """

    name: str = "dify_qna"
    description: str = (
        "Ask a question to a character using Dify AI workflow. "
        "Use this tool when a player wants to ask a specific question "
        "to a character and get an in-character response. "
        "Input should include char_id, act_num, query, model_name, and user_id."
    )
    return_direct: bool = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.args_schema = QnAInput
    
    def _run(
        self,
        char_id: str,
        act_num: int,
        query: str,
        model_name: str,
        user_id: str,
        history: Optional[str] = None,  # Internal parameter only
    ) -> str:
        """
        Execute the Q&A interaction.

        Args:
            char_id: Character ID
            act_num: Act number
            query: Question to ask
            model_name: AI model name
            user_id: User ID
            history: Game history context (internal use only)
            run_manager: Callback manager for tool execution

        Returns:
            Character's response to the question
        """
        try:
            logger.info(f"Q&A for character {char_id}, act {act_num}: {query[:100]}...")

            # Call the Dify Q&A workflow with history context
            answer = call_qna_workflow(
                char_id=char_id,
                act_num=act_num,
                query=query,
                history=history,  # Pass history to service layer
                model_name=model_name,
                user_id=user_id
            )

            logger.info(f"Successfully got answer from character {char_id}")
            return answer
            
        except DifyServiceError as e:
            error_msg = f"Dify service error for character {char_id}: {e}"
            logger.error(error_msg)
            return f"抱歉，{char_id}暂时无法回答这个问题。请稍后再试。"

        except Exception as e:
            error_msg = f"Unexpected error in Q&A for character {char_id}: {e}"
            logger.error(error_msg)
            return f"抱歉，向{char_id}提问时发生了错误。"
    
    async def _arun(
        self,
        char_id: str,
        act_num: int,
        query: str,
        model_name: str,
        user_id: str,
    ) -> str:
        """Async version of the tool execution."""
        # For now, just call the sync version
        # In a production environment, you might want to implement true async calls
        return self._run(char_id, act_num, query, model_name, user_id)


def create_dify_tools() -> list[BaseTool]:
    """
    Create and return a list of all Dify tools.
    
    Returns:
        List of configured Dify tools
    """
    return [
        DifyMonologueTool(),
        DifyQnATool()
    ]


def get_tool_by_name(tool_name: str) -> Optional[BaseTool]:
    """
    Get a specific tool by name.
    
    Args:
        tool_name: Name of the tool to retrieve
        
    Returns:
        Tool instance if found, None otherwise
    """
    tools = create_dify_tools()
    for tool in tools:
        if tool.name == tool_name:
            return tool
    return None

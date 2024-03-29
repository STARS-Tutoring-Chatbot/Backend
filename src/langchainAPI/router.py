from typing import List
import os
from dotenv import load_dotenv
from fastapi import APIRouter
from fastapi import Request

from langchainAPI.example_models import *
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate

from langchain.llms import OpenAI


dotenv_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", ".env")
load_dotenv(dotenv_path)  #

api_key = os.getenv("API_KEY")
debug_mode = os.getenv("DEBUG")
jwt_secret = os.getenv("JWT_SECRET")

router = APIRouter()

model = OpenAI(api_key=os.getenv("OPEN_AI_DEV_KEY"))


@router.post("/api/extractor/test/people")
async def postOpenAIExtractor(request: Request):
    request_body = await request.json()
    query = request_body["data"]

    parser = PydanticOutputParser(pydantic_object=ListOfCodeBlocks)

    systemMessage = (
        "You are an expert extraction algorithm. Only extract relevant information from the text. If you do not know the value of an attribute asked to extract return null for the attribute's value.",
    )

    prompt = PromptTemplate(
        template="Answer the user query. Here is a system message\n{systemMessage}\n{format_instructions}\n{query}\n",
        input_variables=["query"],
        partial_variables={
            "format_instructions": parser.get_format_instructions(),
            "systemMessage": str(systemMessage),
        },
    )
    chain = prompt | model | parser
    res = chain.invoke({"query": query})

    return {
        "Type": "test",
        "query": request_body,
        "result": "result",
        "result": res,
    }


@router.post("/api/extractor/test/isCamelCase")
async def isCamelCase(request: Request):
    request_body = await request.json()
    query = request_body["data"]

    parser = PydanticOutputParser(pydantic_object=ListOfCodeBlocks)

    systemMessage = (
        "You are an expert extraction algorithm. Only extract relevant information from the text. If you do not know the value of an attribute asked to extract return null for the attribute's value.",
    )

    prompt = PromptTemplate(
        template="Answer the user query. Here is a system message\n{systemMessage}\n{format_instructions}\n{query}\n",
        input_variables=["query"],
        partial_variables={
            "format_instructions": parser.get_format_instructions(),
            "systemMessage": str(systemMessage),
        },
    )
    chain = prompt | model | parser
    res = chain.invoke({"query": query})

    return {
        "Type": "test",
        "query": request_body,
        "result": "result",
        "result": res,
    }

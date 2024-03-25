import os
from openai import OpenAI
from supabase import Tables
from typing import List, Dict, Union
from uuid import uuid4
from datetime import datetime, timedelta

supabase_key = os.getenv("VITE_SUPABASE_KEY")
supabase_url = os.getenv("VITE_SUPABASE_URL")


openai = OpenAI(
    apiKey=supabase_key,
    dangerouslyAllowBrowser=True
)
async def getOpenAIResponse(
    messages: List[Tables["Messages"]],
    conversationid: str
) -> Dict[str, Union[Tables["OpenAI-Responses"], None]]:
    strippedMessages = [{
        "role": message["role"],
        "content": message["content"]
    } for message in messages]

    message = None
    metadata = None

    print(strippedMessages)

    testPrompt = "Hello! You are my personal coding assistant! Whenever outputing code, please do not say the answer directly. Instead lead me in the correct direction! Also have a very nice tone :)"

    res = openai.chat.completions.create(
        messages=[{"role": "system", "content": testPrompt}, *strippedMessages],
        model="gpt-3.5-turbo",
        n=1
    )

    print("RES = ", res)

    messageID = str(uuid4())
    metadataID = str(uuid4())
    time = (datetime.utcnow() + timedelta(minutes=-datetime.utcnow().utcoffset().total_seconds() // 60)).replace(microsecond=0).isoformat()

    message = {
        "role": res.choices[0].message.role,
        "content": res.choices[0].message.content,
        "conversation_id": conversationid,
        "created_at": time,
        "id": messageID
    }

    metadata = {
        "chat_completion_id": res.id,
        "completion_tokens": res.usage.completion_tokens if res.usage else None,
        "created": time,
        "id": metadataID,
        "message": messageID,
        "model": res.model,
        "prompt_tokens": res.usage.prompt_tokens if res.usage else None,
        "system_fingerprint": res.system_fingerprint if hasattr(res, "system_fingerprint") else None,
        "total_tokens": res.usage.total_tokens if res.usage else None
    }

    return {
        "message": message,
        "metadata": metadata
    }

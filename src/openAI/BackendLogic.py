import os
from openai import OpenAI
from typing import List
from uuid import uuid4
from datetime import datetime

from openAI.models import ClientMessages

supabase_key = os.getenv("VITE_SUPABASE_KEY")
supabase_url = os.getenv("VITE_SUPABASE_URL")


openai = OpenAI(
    api_key=os.getenv("OPEN_AI_DEV_KEY"),
)


def getOpenAIResponse(messages: List[ClientMessages], conversation_id: str, model: str):

    print(model)

    strippedMessages = map(lambda x: {"role": x.role, "content": x.content}, messages)
    systemMessage = [
        {
            "role": "system",
            "content": "Hello! You are my personal coding assistant! Whenever outputing code, please do not say the answer directly. Instead lead me in the correct direction! Also, every response MUST adhere to markdown. To keep things organized try to make use of headings and bullets. Additionally, any code that is output MUST be in a code block. For example: ```python print('Hello World!') ``` Also code blocks MUST BE seperated by at least a single line. Additionally, math equations must be in latex format. For example: $$y = mx + b$$",
        }
    ]
    strippedMessages = list(strippedMessages)

    allMessages = systemMessage + strippedMessages
    res = openai.chat.completions.create(
        messages=allMessages,  # type: ignore
        model=model.lower(),
        n=1,  # type: ignore
    )

    messageID = str(uuid4())
    metadataID = str(uuid4())

    time = (datetime.now()).replace(microsecond=0).isoformat()

    message = {
        "role": res.choices[0].message.role,
        "content": res.choices[0].message.content,
        "conversation_id": conversation_id,
        "created_at": time,
        "id": messageID,
    }

    metadata = {
        "chat_completion_id": res.id,
        "completion_tokens": res.usage.completion_tokens if res.usage else None,
        "created": time,
        "id": metadataID,
        "message": messageID,
        "model": res.model,
        "prompt_tokens": res.usage.prompt_tokens if res.usage else None,
        "system_fingerprint": (
            res.system_fingerprint if hasattr(res, "system_fingerprint") else None
        ),
        "total_tokens": res.usage.total_tokens if res.usage else None,
    }

    return {"message": message, "metadata": metadata}

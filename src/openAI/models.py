import json
from dataclasses import dataclass, asdict
from typing import List, Optional

@dataclass
class Message:
    content: str
    role: str

@dataclass
class Choice:
    finish_reason: str
    index: int
    message: Message
    logprobs: Optional[dict]

@dataclass
class Usage:
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int

@dataclass
class OpenAIResponse:
    choices: List[Choice]
    created: int
    id: str
    model: str
    object: str
    usage: Usage


def parse_openai_response(json_data):
    # Convert JSON to Python object
    data = json.loads(json_data)

    # Convert nested dictionaries to data class instances
    choices = [Choice(**choice) for choice in data['choices']]
    usage = Usage(**data['usage'])

    # Create and return an instance of OpenAIResponse
    return OpenAIResponse(
        choices=choices,
        created=data['created'],
        id=data['id'],
        model=data['model'],
        object=data['object'],
        usage=usage
    )

# Example usage:
raw_json_data = '''
{
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "message": {
        "content": "The 2020 World Series was played in Texas at Globe Life Field in Arlington.",
        "role": "assistant"
      },
      "logprobs": null
    }
  ],
  "created": 1677664795,
  "id": "chatcmpl-7QyqpwdfhqwajicIEznoc6Q47XAyW",
  "model": "gpt-3.5-turbo-0613",
  "object": "chat.completion",
  "usage": {
    "completion_tokens": 17,
    "prompt_tokens": 57,
    "total_tokens": 74
  }
}
'''

openai_response = parse_openai_response(raw_json_data)

# Accessing attributes
print(openai_response.choices[0].message.content)
print(openai_response.usage.total_tokens)

import os
import json
from typing import Type, TypeVar, Optional
from pydantic import BaseModel, ValidationError
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

T = TypeVar("T", bound=BaseModel)

class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found")
        self.client = OpenAI(api_key=self.api_key)

    def call_with_schema(self, system_prompt: str, user_prompt: str, schema: Type[T], model: str = "gpt-4o-mini", retries: int = 1) -> T:
        """
        Calls the LLM and enforces a Pydantic schema.
        Handles one retry automatically on validation failure.
        """
        for attempt in range(retries + 1):
            try:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    response_format={"type": "json_object"}
                )
                
                content = response.choices[0].message.content
                data = json.loads(content)
                return schema.model_validate(data)
            
            except (json.JSONDecodeError, ValidationError) as e:
                if attempt < retries:
                    # Optional: Add error feedback to the user_prompt for the retry
                    user_prompt += f"\n\nPrevious attempt failed validation: {str(e)}. Please try again and ensure strict adherence to the schema."
                    continue
                else:
                    raise e
            except Exception as e:
                raise e

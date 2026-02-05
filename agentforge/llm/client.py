import os
import json
import google.generativeai as genai
from typing import Type, TypeVar, Optional
from pydantic import BaseModel, ValidationError
from dotenv import load_dotenv

load_dotenv()

T = TypeVar("T", bound=BaseModel)

class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment")
        
        genai.configure(api_key=self.api_key)
        
        # Try to find a working model
        default_model = 'models/gemini-1.5-flash'
        try:
            # Check availability
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            if default_model in available_models:
                self.model_name = default_model
            else:
                # Fallback to the first available gemini model
                gemini_models = [m for m in available_models if 'gemini' in m]
                self.model_name = gemini_models[0] if gemini_models else 'gemini-pro'
        except:
            self.model_name = 'gemini-1.5-flash'
            
        self.model = genai.GenerativeModel(self.model_name)

    def call_with_schema(self, system_prompt: str, user_prompt: str, schema: Type[T], retries: int = 1) -> T:
        """
        Calls Google Gemini and enforces a Pydantic schema using JSON prompting.
        Handles one retry automatically on validation failure.
        """
        # Combine system and user prompts as Gemini handles it slightly differently 
        # but we can pass system_instruction to the model constructor or just prepend it.
        # For simplicity and compatibility with older Gemini, we'll prepend.
        full_prompt = f"{system_prompt}\n\nUser Request: {user_prompt}\n\nOutput MUST be a valid JSON object matching the schema."

        for attempt in range(retries + 1):
            try:
                response = self.model.generate_content(
                    full_prompt,
                    generation_config=genai.types.GenerationConfig(
                        response_mime_type="application/json",
                    )
                )
                
                content = response.text
                data = json.loads(content)
                return schema.model_validate(data)
            
            except (json.JSONDecodeError, ValidationError) as e:
                if attempt < retries:
                    user_prompt += f"\n\nPrevious attempt failed validation: {str(e)}. Please ensure strict adherence to the JSON schema."
                    continue
                else:
                    raise e
            except Exception as e:
                raise e

import logging  # noqa: N999

import cohere

from ..LLMEnums import CohereEnums, DocumentTypeEnum
from ..LLMInterface import LLMInterface


class ChohereProvider(LLMInterface):

    def __init__(self, api_key: str,
                     default_input_max_char: int = 1000,
                     default_generation_output_tokens: int = 1000,
                     default_generation_temp: float = 0.1):
    
        self.api_key = api_key
        self.default_input_max_char = default_input_max_char
        self.default_generation_output_tokens = default_generation_output_tokens
        self.default_generation_temp = default_generation_temp
        
        self.generation_model_id: str | None = None
        self.embedding_model_id: str | None = None
        self.embedding_size: int | None = None

        self.co = cohere.ClientV2(api_key=self.api_key)

        self.logger = logging.getLogger(__name__)

    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id
    
    def set_embedding_model(self, model_id: str, embedding_size: int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size

    def process_text(self, text: str):
        return text[:self.default_input_max_char].strip()

    def generate_text(self, prompt: str, chat_history: list | None = None,
                        max_output_tokens: int | None = None, temp: float | None = None):
        
        if not self.co:
            self.logger.error("Cohere Client was not set")
            return None

        if not self.generation_model_id:
            self.logger.error("Generation Model for Cohere was not set")
            return None

        max_output_tokens = max_output_tokens if max_output_tokens else self.default_generation_output_tokens
        temp = temp if temp else self.default_generation_temp

        if chat_history is None:
            chat_history= []

        chat_history.append(
            self.construct_prompt(role=CohereEnums.USER.value , prompt=prompt)
        )

        response = self.co.chat(
            model = self.generation_model_id,
            messages = chat_history,
            max_tokens = max_output_tokens,
            temperature = temp
        )

        if not response or not response.message or not response.message.content:
            self.logger.error("Error while generating text with Cohere")
            return None
        
        return response.message.content[0].text

    def embed_text(self, text: str, document_type: str | None = None):

        if not self.co:
            self.logger.error("Cohere Client was not set")
            return None

        if not self.embedding_model_id:
            self.logger.error("Embedding Model for Cohere was not set")
            return None

        input_type = CohereEnums.DOCUMENT.value
        if document_type == DocumentTypeEnum.QUERY.value:
            input_type = CohereEnums.QUERY.value

        response = self.co.embed(
            input = [self.process_text(text)],
            model = self.embedding_model_id,
            input_type = input_type,
            embedding_types = ["float"]

        )

        if not response or not response.embeddings or len(response.embeddings) == 0:
            self.logger.error("Error while embedding text with Cohere")
            return None

        return response.embedding.float[0]

    def construct_prompt(self, prompt:str, role:str):
        return {
            "role" : role,
            "content" : self.process_text(text=prompt)
        }

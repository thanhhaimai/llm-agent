from google import genai
from google.genai import types
from pydantic import BaseModel

MAX_OUTPUT_TOKENS = 8192
MODEL_NAME = "gemini-2.0-flash"


class GeminiClient:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.files = []

    def upload_file(self, file_path: str, file_name: str | None = None):
        file: types.File = self.client.files.upload(
            file=file_path,
            config=types.UploadFileConfig(name=file_name, display_name=file_name),
        )
        self.files.append(file)

    def delete_all_files(self):
        files = self.client.files.list()
        for file in files:
            if file.name is not None:
                self.client.files.delete(name=file.name)

    def _get_contents(self, prompt: str, request_model: BaseModel | None):
        if request_model is not None:
            request_content = request_model.model_dump_json(exclude_none=True)
            return [prompt, *self.files, request_content]
        else:
            return [prompt, *self.files]

    def _get_config(self, response_schema: type[BaseModel] | None):
        if response_schema is not None:
            return types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=response_schema,
                max_output_tokens=MAX_OUTPUT_TOKENS,
            )
        else:
            return types.GenerateContentConfig(
                response_mime_type="text/plain",
                max_output_tokens=MAX_OUTPUT_TOKENS,
            )

    def execute_stream(
        self,
        prompt: str,
        request_model: BaseModel | None = None,
        response_schema: type[BaseModel] | None = None,
    ):
        for chunk in self.client.models.generate_content_stream(
            model=MODEL_NAME,
            contents=self._get_contents(prompt=prompt, request_model=request_model),
            config=self._get_config(response_schema=response_schema),
        ):
            yield chunk.text

    def execute(
        self,
        prompt: str,
        request_model: BaseModel | None = None,
        response_schema: type[BaseModel] | None = None,
    ):
        contents = self._get_contents(prompt=prompt, request_model=request_model)
        config = self._get_config(response_schema=response_schema)
        response = self.client.models.generate_content(
            model=MODEL_NAME,
            contents=contents,
            config=config,
        )
        return response.text

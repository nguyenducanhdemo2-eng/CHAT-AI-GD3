import inspect
from google import genai
print('genai module:', genai)
print('Client signature:', inspect.signature(genai.Client))
print('generate_content signature:', inspect.signature(genai.Client.models.generate_content))

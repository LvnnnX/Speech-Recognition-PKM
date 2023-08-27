import openai
import pathlib,json

BASE_DIR = pathlib.Path(__file__).parent.parent
TOKEN_DIR = BASE_DIR / "token"

with open(f'{TOKEN_DIR}/api_token.json')as f:
    tokens = json.load(f)
    openai.api_key = tokens['OpenAI_API']

def chatgpt(prompt):
    response= openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        temperature=0,
        max_tokens=100
    )
    return response.choices[0].text #tpye: ignore

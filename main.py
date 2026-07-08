import os
import argparse

from dotenv import load_dotenv

from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam, ChatCompletion

def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("There was a problem with the OPENROUTER_API_KEY variable")
    
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()
# Now we can access `args.user_prompt`

    messages: list[ChatCompletionMessageParam] = [
        {
            "role": "user",
            "content": args.user_prompt
        }
    ]

    response: ChatCompletion = client.chat.completions.create(
        model="openrouter/free",
        messages=messages
)
    if response.usage is not None:
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
    else:
        raise RuntimeError("attribute 'usage' of response is None")
    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()

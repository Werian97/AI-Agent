import os
import argparse
from typing import Iterable, cast

from dotenv import load_dotenv
from call_functions import call_function

from openai import OpenAI
from openai.types.chat import ChatCompletion, ChatCompletionMessageFunctionToolCall, ChatCompletionMessage, ChatCompletionMessageParam


def call_a_client():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("There was a problem with the OPENROUTER_API_KEY variable")
    
    return OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

def take_arguments():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument('--verbose', action='store_true', help="Enable verbose output")

    return parser.parse_args()

def check_for_usage(response: ChatCompletion, args: argparse.Namespace):
            if response.usage is not None:
                if args.verbose:
                    print(f"User prompt: {args.user_prompt}")
                    print(f"Prompt tokens: {response.usage.prompt_tokens}")
                    print(f"Response tokens: {response.usage.completion_tokens}")
            else:
                raise RuntimeError("attribute 'usage' of response is None")
            return None

def execute_order(message: ChatCompletionMessage, args: argparse.Namespace, messages: list[ChatCompletionMessageParam]):
    if message.tool_calls is not None:    
        for tool_call in message.tool_calls:
            if isinstance(tool_call, ChatCompletionMessageFunctionToolCall):
                result_message: dict
                if args.verbose:
                    result_message = call_function(tool_call, True)
                    content = result_message.get("content", None)
                    if content is None:
                        raise Exception("No content produced")
                    print(f"-> {content}")
                else:
                    result_message = call_function(tool_call)
                messages.append(cast(ChatCompletionMessageParam,result_message))
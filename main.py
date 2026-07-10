import sys

import prompts

from openai.types.chat import ChatCompletionMessageParam, ChatCompletion, ChatCompletionMessage

from call_functions import available_functions
from utility_functions import call_a_client, check_for_usage, execute_order, take_arguments
from typing import cast

from config import MAX_ITERATIONS

def main():
    client = call_a_client()
    args = take_arguments()
# Now we can access `args.user_prompt`

    messages: list[ChatCompletionMessageParam] = [
        {"role": "system", "content": prompts.system_prompt},
        {"role": "user", "content": args.user_prompt}
    ]
    for _ in range(MAX_ITERATIONS):
        response: ChatCompletion = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions
        )
        check_for_usage(response, args)
        message: ChatCompletionMessage = response.choices[0].message
        messages.append(cast(ChatCompletionMessageParam, message))
        if message.tool_calls is None:
            print(message.content) #answer content
            return None
        else:
            execute_order(message, args, messages)
    print(f"The agent couldn't finish the work within {MAX_ITERATIONS} iterations")
    sys.exit(1)


if __name__ == "__main__":
    main()

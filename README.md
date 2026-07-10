# AI-Agent

This project uses the OpenAI Python SDK together with OpenRouter to interact with large language models through an OpenAI-compatible REST API.

## Usage

The agent is operated through the terminal. To invoke the agent run
```bash
python3 main.py "your-request"
```
Run the command _from the root_ directory, not from the calculator directory. Write a request in English inside quotation marks.
The agent will inspect the project, modify the necessary files, and execute the updated code when required.

## What the agent can do

The agent has access **only** to the content of the calculator directory \(for safety reasons\) and it can
1. list the content of a directory;
2. read the content of a file;
3. overwrite existing files or create brand new files or directories;
4. execute python scripts.

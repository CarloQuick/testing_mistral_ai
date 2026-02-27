import os
from mistralai import Mistral


def prompt_mistral(user_input, client, model):

    chat_response = client.chat.complete(
        model= model,

        messages = [
            {"role": "system", "content": "Convert the user's prompt into bash commands. Respond with ONLY the command. No explanation, no markdown, no notes."},
            # grep
            {"role": "user", "content": "Can you find sleeping processes on my machine?"},
            {"role": "assistant", "content": "ps aux | grep sleep"},
            {"role": "user", "content": "Return past commands using the string mv"},
            {"role": "assistant", "content": "history | grep mv"},
            {"role": "user", "content": "Find the occurences of the exact term 'Python' in report.txt"},
            {"role": "assistant", "content": "grep \"Python\" report.txt"},
            {"role": "user", "content": "Find the occurences of the term 'Python' regardless of case in report.txt"},
            {"role": "assistant", "content": "grep -i \"Python\" report.txt"},
            # ls
            {"role": "user", "content": "List the contents of the directory ./dev."},
            {"role": "assistant", "content": "ls ./dev"},
            {"role": "user", "content": "List the contents of the current directory sorted by modification time - newest first."},
            {"role": "assistant", "content": "ls -t"},
            {"role": "user", "content": "List the contents of the current directory sorted by modification time - oldest first."},
            {"role": "assistant", "content": "ls -tr"},
            {"role": "user", "content": "List the hidden and unhidden contents of the directory ./dev."},
            {"role": "assistant", "content": "ls -a ./dev"},
            {"role": "user", "content": "List the hidden and unhidden contents of the current directory sorted by modification time - newest first."},
            {"role": "assistant", "content": "ls -at"},
            {"role": "user", "content": "List contents of the current directory that containe any variation of \"PYTHON\"."},
            {"role": "assistant", "content": "ls | grep -i \"PYTHON\""},
            {"role": "user", "content": "List he hidden and unhidden contents at ./dev named any variation of 'rust', including hidden ones. Newest on top."},
            {"role": "assistant", "content": "ls -at ./dev | grep -i \"rust\""},
            {"role": "user", "content": user_input},
        ], stream=False
        )

    return chat_response.choices[0].message.content

def tiny_agent():
    
    api_key: str | None = os.getenv("MISTRAL_API_KEY")

    model: str = "ministral-8b-2512"
    client: Mistral = Mistral(api_key=api_key)
    prompt: str = "\nWhat would you like in bash? (type 'quit' to stop): "

    while True:
        user_input: str = input(prompt)
        if user_input.lower() == 'quit':
            break
        response = prompt_mistral(user_input, client, model)
        print(response)
    
    print("Nice talking to you.")


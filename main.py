from openai import OpenAI
import time
context = []


with open("api_key.txt", 'r') as file:
    api_key = file.read()

client = OpenAI(api_key=api_key)

def get_transcript():
    transcript = ""
    for message in context:
        transcript += f"{message['name']}: {message['content']}"

    return transcript
def get_prompt():
    prompt = f"""
    Character is a conversational person.
    
    Here is a conversation transcript between Nico and Character:
    {get_transcript()}
    
    How would Character continue his last sentence?
    Character: <insert line>
    """

    return prompt

def generate_response():
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": get_prompt()}],
        stream=True
    )
    sentence = ""
    sentence_end = ['.', '!', '?']
    last_token = None
    for chunk in response:
        token = chunk.choices[0].delta.content
        if token is None:
            break

        if last_token in sentence_end:
            sentence = sentence.strip()
            context.append({"role": "assistant", "content": sentence, "name": "Character"})
            print(sentence)
            generate_response()
        last_token = token
        sentence += token

def get_user_response():
    prompt = input()
    context.append({"role": "user", "content": prompt, "name": "Nico"})

while True:
    get_user_response()
    generate_response()

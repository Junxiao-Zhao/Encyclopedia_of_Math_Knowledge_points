import regex as re
import configparser
from time import sleep

from openai import OpenAI

config = configparser.RawConfigParser()
config.read('./config/main.cfg')

client = OpenAI()
assistant = client.beta.assistants.retrieve(config.get('assistant', 'id'))
thread = client.beta.threads.create()


def analyze(question: str):

    _ = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=("List identified knowledge points with corresponding IDs "
                 f"from this question: ```{question}```"))
    run = client.beta.threads.runs.create(thread_id=thread.id,
                                          assistant_id=assistant.id)

    run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    while run.status == 'in_progress':
        sleep(10)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id,
                                                run_id=run.id)
    # print(run.status)
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    answer = messages.data[0].content[0].text.value
    answer = re.sub(r'【\d+†source】', '', answer)

    return answer


while True:
    question = input('Enter question here:\n\n')
    print()
    if question == 'exit':
        break

    print(analyze(question))
    print()

client.beta.threads.delete(thread.id)

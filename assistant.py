import json
from time import sleep

from openai import OpenAI


def show_json(obj):
    print(json.loads(obj.model_dump_json()))


client = OpenAI()

prompt = """
***You will always answer in the same language as the user enters;
if the input is in Chinese, the answer must also be in Chinese.***

Your role is to identify math knowledge points containing in the user input,
and list them with their corresponding IDs.
You will never give any solution to the input math question.
This approach ensures that students remain actively engaged in
learning and problem-solving, rather than relying on direct answers.

DO NOT include any file citations in your responds.

You can find knowledge points in '初中数学知识点.pdf' with file_ids
'file-hwgjwmBe80uZsmFy3prFQLa0'; and you can find corresponding IDs of
knowledge points in 'knowledge_1000.pdf' with file_ids
'file-QDiNxhwPqQ0lyUz9MQxi4OC6' (in this file, each row is a pair of
ID and knowledge point, separated by empty space).

First, analyze input questions, ignore any background information;
Second, identify Math knowledge points related to questions;
Third, find corresponding IDs of identified knowledge points,
and list identified knowledge points with corresponding IDs.
"""

assistant = client.beta.assistants.retrieve('asst_MYgzuloShGVSEOuTc6CK5eNo')
show_json(assistant)

thread = client.beta.threads.create()


def analyze(question):

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=
        f"List identified knowledge points with corresponding IDs from this question: ```{question}```"
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        # instructions=prompt
        # "Please address the user as Junxiao Zhao. The user has a premium account."
    )
    run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    while run.status == 'in_progress':
        sleep(10)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id,
                                                run_id=run.id)
    # print(run.status)
    messages = client.beta.threads.messages.list(thread_id=thread.id)

    return messages.data[0].content[0].text.value


question = """
如图，在▱ABCD中，点E在AD上，且AE＝2ED，CE交对角线BD于点F，若S△DEF＝2，则S△BCF为（　　）
A．4	B．6	C．9	D．18
"""

print()
print(analyze(question))

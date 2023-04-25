


import os
import subprocess
import json
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import UnstructuredFileLoader
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.text_splitter import TokenTextSplitter
from dotenv import load_dotenv


load_dotenv()
with open("./docs/input.txt", "r") as f:
    doc = f.read()
openai_api_key = os.getenv("OPENAI_API_KEY")
text_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_text(doc)
chat = ChatOpenAI(temperature=0)
with open("./docs/input.json", "r") as f:
    examples = json.load(f)
messages = [
    SystemMessage(content="""
    You are a helpful assistant that responds to support ticket requests.
    Here are some examples of support ticket requests:{examples}.
    Always sign off as Richard
    Provide your responses in valid JSON format with this schema
    "response":[{
    "draft_email":"[DRAFT_EMAIL_RESPONSE]",
    "user_email":"[USER_EMAIL_RESPONSE]",
    "draft_email_subject":"[DRAFT_EMAIL_SUBJECT_RESPONSE]"
    }]
    review your response and ensure it is valid JSON before submitting.
    """),
    HumanMessage(content=doc)
]
content = chat(messages).content
#print(content)
json_response = json.loads(content)
print(json_response)
user_email = json_response['response'][0]['user_email']
draft_email = json_response['response'][0]['draft_email']
draft_email_subject = json_response['response'][0]['draft_email_subject']
print(user_email, draft_email_subject, draft_email)
with open ("./docs/output.txt", "w") as f:
    f.write(user_email + "\n" + draft_email_subject+ "\n" + draft_email)
def send_draft_email(user_email, draft_email, draft_email_subject):
    subprocess.Popen(["python", "./scripts/gmail.py", "--draft_email", draft_email, "--user_email", user_email, "--draft_email_subject", draft_email_subject], bufsize=1024)
result = send_draft_email(user_email, draft_email, draft_email_subject)
print(result)

from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List
import json
import os
os.environ['HUGGINGFACEHUB_API_TOKEN'] = "api-key"
load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-R1",
    task="text-generation",
)
model = ChatHuggingFace(llm=llm, verbose=True)

system_prompt = """
The user will provide a multiple-choice question (MCQ) in plain text. Please parse the question, options, and the correct answer. 
Output the result in the following valid JSON format:

EXAMPLE INPUT:
What is the capital of India? 
A) Berlin 
B) Madrid 
C) New Delhi 
D) Rome 
Answer: C

EXAMPLE JSON OUTPUT:
{{
  "question": "What is the capital of India?",
  "options": ["Berlin", "Madrid", "New Delhi", "Rome"],
  "answer": 3
}}
"""
prompt = ChatPromptTemplate([
    ("system",system_prompt),
    ("user","Give me 5 MCQs with correct answers on {topic}")
])

class MCQ(BaseModel):
    question: str
    options: List[str] = Field(..., min_items=4, max_items=4)
    answer: int

model_with_structure = model.with_structured_output(MCQ,method='json_mode')


def fetchQuestions(topic):
    response = model_with_structure.invoke(prompt.invoke({"topic":topic}))
    # print(type(response))
    json_output = json.dumps(response, indent=2)
    print(json_output)

    return response
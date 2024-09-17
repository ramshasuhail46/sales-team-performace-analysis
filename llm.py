from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.memory import ConversationSummaryBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.callbacks.base import BaseCallbackHandler

from dotenv import load_dotenv
import os

load_dotenv()

chat_model = ChatGroq(
    temperature=0.6,
    model="llama-3.1-70b-versatile",
    api_key=os.getenv('API_KEY'),
    streaming=True,
    callbacks=[BaseCallbackHandler()]
)

memory = ConversationSummaryBufferMemory(
    llm=chat_model, 
    memory_key="chat_history",  
    return_messages=True, 
    max_token_limit=200,
    summary_prompt="Summarize the key points of the conversation so far.",
)

def create_sales_insight_prompt(data_type):
    if data_type == "individual":
        prompt_template = ChatPromptTemplate(
            messages=[
                SystemMessagePromptTemplate.from_template(
                    "You are a sales analyst with expertise in generating insights from sales data. "
                    "Your task is to provide insights based on the following data for an individual sales representative.\n"
                    "Data: {data}\n"
                    "Generate insights focusing on performance metrics such as leads taken, tours booked, revenue confirmed, and more. "
                    "Offer suggestions for improvement where applicable."
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessagePromptTemplate.from_template("{question}")
            ]
        )
    elif data_type == "team":
        prompt_template = ChatPromptTemplate(
            messages=[
                SystemMessagePromptTemplate.from_template(
                    "You are a sales analyst with expertise in generating insights from sales data. "
                    "Your task is to provide insights based on the following data for the sales team as a whole.\n"
                    "Data: {data}\n"
                    "Generate insights on overall team performance, including aggregated metrics like total leads, tours booked, and average revenue. "
                    "Highlight areas where the team is excelling and areas that need improvement."
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessagePromptTemplate.from_template("{question}")
            ]
        )
    elif data_type == "organization":
        prompt_template = ChatPromptTemplate(
            messages=[
                SystemMessagePromptTemplate.from_template(
                    "You are a sales analyst with expertise in generating insights from sales data. "
                    "Your task is to provide insights based on the following data for the entire organization.\n"
                    "Data: {data}\n"
                    "Generate insights on the overall performance of the organization, including high-level metrics and trends. "
                    "Provide recommendations for strategic improvements and areas of focus."
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessagePromptTemplate.from_template("{question}")
            ]
        )
    else:
        raise ValueError("Invalid data type. Must be 'individual', 'team', or 'organization'.")
    
    return prompt_template

def chat(data, data_type, input):
    prompt_template = create_sales_insight_prompt(data_type)
    
    conversation = LLMChain(
        llm=chat_model,
        prompt=prompt_template,
        verbose=False,
        memory=memory
    )

    for output in conversation.stream({"data": data, "question": input}):
        return output['text']

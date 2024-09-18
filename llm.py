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
import json

load_dotenv()


class SalesInsightChat:
    def __init__(self):
        self.chat_model = ChatGroq(
            temperature=0.6,
            model="llama-3.1-70b-versatile",
            api_key=os.getenv('API_KEY'),
            # streaming=True,
            callbacks=[BaseCallbackHandler()]
        )

        self.memory = ConversationSummaryBufferMemory(
            llm=self.chat_model,
            memory_key="chat_history",
            input_key='question',  # Specify the user input key here
            return_messages=True,
            max_token_limit=200,
            summary_prompt="Summarize the key points of the conversation so far.",
        )

    def create_sales_insight_prompt(self, data_type):
        if data_type == "individual":
            prompt_template = ChatPromptTemplate(
                input_variables=['data', 'chat_history', 'question'],
                messages=[
                    SystemMessagePromptTemplate.from_template(
                        "You are a sales analyst with expertise in generating insights from sales data. "
                        "Your task is to provide detailed performance analysis and feedback for the specified sales representative.\n"
                        "Data: {data}\n"
                        "Offer suggestions for improvement where applicable."
                    ),
                    MessagesPlaceholder(variable_name="chat_history"),
                    HumanMessagePromptTemplate.from_template("{question}")
                ]
            )
        elif data_type == "team":
            prompt_template = ChatPromptTemplate(
                input_variables=['data', 'chat_history', 'question'],
                messages=[
                    SystemMessagePromptTemplate.from_template(
                        "You are a sales analyst with expertise in generating insights from sales data. "
                        "Your task is to provide a summary of the sales team's overall performance.\n"
                        "Data: {data}\n"
                        "Generate insights on overall team performance, including aggregated metrics like total leads, tours booked, and average revenue. "
                        "Highlight areas where the team is excelling and areas that need improvement."
                    ),
                    MessagesPlaceholder(variable_name="chat_history"),
                    HumanMessagePromptTemplate.from_template("{question}")
                ]
            )
        elif data_type == "time period":
            prompt_template = ChatPromptTemplate(
                input_variables=['data', 'chat_history', 'question'],
                messages=[
                    SystemMessagePromptTemplate.from_template(
                        "You are a sales analyst with expertise in generating insights from sales data. "
                        "Your task is to analyze sales data over the specified time period to identify trends and forecast future performance.\n"
                        "Data: {data}\n"
                        "Generate insights on the overall performance of the organization, including high-level metrics and trends. "
                        "Provide recommendations for strategic improvements and areas of focus."
                    ),
                    MessagesPlaceholder(variable_name="chat_history"),
                    HumanMessagePromptTemplate.from_template("{question}")
                ]
            )
        else:
            raise ValueError(
                "Invalid data type. Must be 'individual', 'team', or 'organization'."
            )

        return prompt_template

    def chat(self, data, data_type, input_text):
        prompt_template = self.create_sales_insight_prompt(data_type)

        conversation = LLMChain(
            llm=self.chat_model,
            prompt=prompt_template,
            verbose=False,
            memory=self.memory
        )
        output = conversation.invoke({"question": input_text, "data": data})
        return output['text']

from langchain_openai import AzureChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType
from langchain.tools import StructuredTool
from agent.tool import search_services_by_type, book_appointment_by_input
import os

llm = AzureChatOpenAI(
    openai_api_base="https://amity-ai.openai.azure.com",
    openai_api_version="2025-01-01-preview",
    deployment_name="gpt-4o",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0
)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

tools = [
    StructuredTool.from_function(
        name="SearchService",
        func=search_services_by_type,
        description="Search for healthcare services by name and location. Input should include the service type and optional location."
    ),
    StructuredTool.from_function(
        name="BookAppointment",
        func=book_appointment_by_input,
        description="Book a healthcare service by specifying the option number from the last shown list."
    )
]

agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    memory=memory,
    verbose=True
)

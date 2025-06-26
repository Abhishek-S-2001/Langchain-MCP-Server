from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import Tool, initialize_agent
from agent.tool import search_services_by_type, book_appointment_by_input
import os

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.5,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

tools = [
    Tool(
        name="SearchService",
        func=search_services_by_type,
        description="Search for a healthcare service by name. Input should be the service type, like 'X-Ray'."
    ),
    Tool(
        name="BookAppointment",
        func=book_appointment_by_input,
        description="Book an appointment using user and provider info. Input should be JSON string with details."
    )
]

agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent="conversational-react-description",
    memory=memory,
    verbose=True
)

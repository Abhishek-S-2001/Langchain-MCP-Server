from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import Tool, initialize_agent, AgentType
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
        description=(
            "Use this to search for healthcare services. "
            "Try: 'X-Ray in Mumbai', 'vaccination Andheri', 'dental checkup Pune'."
        )
    ),
    Tool(
        name="BookAppointment",
        func=book_appointment_by_input,
        description=(
            "Use to book appointments. Input should be a JSON string with provider_offering_id, user_id, and appointment_date."
        )
    )
]

agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True,
    agent_kwargs={
        "prefix": (
            "You are a helpful AI healthcare assistant. You can search clinics and book appointments for users."
        ),
        "suffix": (
            "Use the tools if needed.\n\n{chat_history}\nHuman: {input}\nAI:"
        )
    }
)

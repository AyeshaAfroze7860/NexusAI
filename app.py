
import streamlit as st
import logging
from uuid import uuid4
from datetime import datetime

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory


# --------------------------------------------------
# 1. APPLICATION CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="NexusAI | Intelligent Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


# --------------------------------------------------
# 2. CUSTOM STYLING
# --------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #f8fafc;
}

.block-container {
    padding-top: 2rem;
    max-width: 1100px;
}

[data-testid="stSidebar"] {
    background-color: #111827;
}

[data-testid="stSidebar"] * {
    color: white;
}

.stChatMessage {
    border-radius: 12px;
    padding: 12px;
}

.welcome-title {
    text-align: center;
    font-size: 38px;
    font-weight: 700;
    color: #2563eb;
    margin-top: 50px;
}

.welcome-text {
    text-align: center;
    color: #64748b;
    font-size: 17px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# 3. APPLICATION HEADER
# --------------------------------------------------

st.title("🤖 NexusAI")
st.caption("Intelligent Conversations | Powered by Local LLM")

st.divider()


# --------------------------------------------------
# 4. SESSION STATE INITIALIZATION
# --------------------------------------------------

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

if "history_store" not in st.session_state:
    st.session_state.history_store = {}


# --------------------------------------------------
# 5. LANGCHAIN MEMORY MANAGEMENT
# --------------------------------------------------

def get_session_history(session_id: str):

    if session_id not in st.session_state.history_store:

        st.session_state.history_store[session_id] = (
            InMemoryChatMessageHistory()
        )

    return st.session_state.history_store[session_id]


# --------------------------------------------------
# 6. CHATBOT INITIALIZATION
# --------------------------------------------------

@st.cache_resource
def create_chatbot(model_name, temperature):

    llm = ChatOllama(
        model=model_name,
        temperature=temperature
    )

    prompt = ChatPromptTemplate.from_messages([

        (
            "system",
            """
            You are NexusAI, an advanced and professional
            AI assistant.

            Your responsibilities:

            1. Provide accurate and relevant information.
            2. Maintain context from previous conversations.
            3. Explain complex topics in simple language.
            4. Give structured and professional responses.
            5. Avoid unnecessary or repetitive information.
            6. Ask for clarification when a question is unclear.
            7. Maintain a friendly and respectful tone.

            Use the conversation history to understand
            the user's previous questions and references.
            """
        ),

        MessagesPlaceholder(variable_name="history"),

        ("human", "{question}")

    ])

    chain = prompt | llm

    chatbot = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="question",
        history_messages_key="history"
    )

    return chatbot


# --------------------------------------------------
# 7. SIDEBAR SETTINGS
# --------------------------------------------------

with st.sidebar:

    st.title("⚙️ Settings")

    st.divider()

    st.subheader("Model Configuration")

    model_name = st.selectbox(
        "Select Local LLM",
        ["llama3.2", "llama3.1", "mistral"]
    )

    temperature = st.slider(
        "Response Creativity",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1
    )

    st.divider()

    st.subheader("System Information")

    st.write("🤖 Model:", model_name)
    st.write("🧠 Memory: Enabled")
    st.write("💻 Runtime: Local Ollama")
    st.write("🔒 Processing: Local LLM")

    st.divider()

    st.subheader("Conversation")

    st.write(
        f"Total Messages: {len(st.session_state.messages)}"
    )

    if st.button("🗑️ Clear Conversation", use_container_width=True):

        st.session_state.messages = []

        st.session_state.history_store.pop(
            st.session_state.session_id,
            None
        )

        st.rerun()

    if st.button("➕ New Conversation", use_container_width=True):

        st.session_state.session_id = str(uuid4())
        st.session_state.messages = []

        st.rerun()

    st.divider()

    st.caption("NexusAI | Local AI Assistant")
    st.caption("Built with Streamlit, LangChain & Ollama")


# --------------------------------------------------
# 8. INITIALIZE CHATBOT
# --------------------------------------------------

chatbot = create_chatbot(model_name, temperature)


# --------------------------------------------------
# 9. WELCOME SCREEN
# --------------------------------------------------

if not st.session_state.messages:

    st.markdown(
        '<div class="welcome-title">Welcome to NexusAI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="welcome-text">'
        'Your intelligent assistant for learning, '
        'problem-solving and everyday conversations.'
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")

    st.markdown("### What can I help you with?")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("💡 **Learn**\n\nUnderstand complex concepts.")

    with col2:
        st.info("💻 **Develop**\n\nGet help with programming.")

    with col3:
        st.info("🧠 **Explore**\n\nAsk questions and explore ideas.")


# --------------------------------------------------
# 10. DISPLAY CHAT HISTORY
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# --------------------------------------------------
# 11. USER INPUT AND RESPONSE GENERATION
# --------------------------------------------------

user_input = st.chat_input(
    "Message NexusAI..."
)

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):

        with st.spinner("NexusAI is generating a response..."):

            try:

                response = chatbot.invoke(
                    {"question": user_input},

                    config={
                        "configurable": {
                            "session_id": st.session_state.session_id
                        }
                    }
                )

                answer = response.content

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as error:

                logger.exception("Chatbot response generation failed")

                st.error(
                    "Unable to generate a response. "
                    "Please verify that Ollama is running "
                    "and the selected model is installed."
                )

                st.caption(
                    "Technical details: " + str(error)
                )


import os
import gradio as gr
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain.memory import ConversationBufferMemory
from langchain.tools import tool
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.llms import Together
from langchain.schema import Document

#
os.environ["TOGETHER_API_KEY"] = "988d73e388e1b6c2e5c4b1517b2a07f4c21dd8d9b48f585da410cc6094a6c6d4"

llm = Together(
    model="togethercomputer/llama-2-70b-chat",
    temperature=0.7,
    max_tokens=512
)

memory = ConversationBufferMemory(memory_key="chat_history")

# ✅ Step 5: Setup Vectorstore (RAG)
def setup_vectorstore():
    docs = [
        "Founders with mismatched values often split when faced with stress.",
        "Always draft a founder agreement outlining equity, decision-making, and exit paths.",
        "Startup founders need aligned risk appetites to navigate early volatility.",
        "Communication breakdowns are the top cause of cofounder splits.",
        "When in doubt, create role-based boundaries to reduce friction.",
    ]
    documents = [Document(page_content=doc) for doc in docs]
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return Chroma.from_documents(documents, embeddings, collection_name="founder_docs")

db = setup_vectorstore()
rag_chain = RetrievalQA.from_chain_type(llm=llm, retriever=db.as_retriever(), chain_type="stuff")

# ✅ Step 6: Define Tools with Required Docstrings
@tool
def personality_profiling(input: str) -> str:
    """Analyze the MBTI, values, and risk appetite of the founder based on their input."""
    prompt = f"Analyze the MBTI, values, and risk appetite in this founder input: {input}"
    return llm.invoke(prompt)

@tool
def simulate_scenario(input: str) -> str:
    """Simulate a startup decision-making scenario between two founders."""
    return llm.invoke(f"Simulate a scenario of conflict or collaboration between founders: {input}")

@tool
def detect_conflict(input: str) -> str:
    """Detect potential co-founder misalignment, tension, or personality clashes."""
    return llm.invoke(f"Detect co-founder misalignment or tension based on: {input}")

@tool
def alignment_report(input: str) -> str:
    """Generate a RAG-based alignment report including suggestions and best practices."""
    return rag_chain.run(f"Generate cofounder best practices or improvement plan based on: {input}")

# ✅ Step 7: Combine Tools into Agent
tools = [personality_profiling, simulate_scenario, detect_conflict, alignment_report]
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, memory=memory, verbose=True)

# ✅ Step 8: Gradio UI
def cofounder_analysis(input_text):
    return agent.run(input_text)

iface = gr.Interface(
    fn=cofounder_analysis,
    inputs=gr.Textbox(lines=5, placeholder="Enter founder traits, scenarios, or issues here..."),
    outputs=gr.Textbox(),
    title="🧠 Cofounder Personality Clash Detector (Together AI)",
    description="Analyze MBTI traits, simulate conflict scenarios, detect cofounder tension, and get enriched RAG suggestions."
)

# ✅ Step 9: Launch UI with Public Link
iface.launch(share=True)

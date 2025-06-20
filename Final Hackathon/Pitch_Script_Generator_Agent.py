import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.tools import tool

os.environ["GOOGLE_API_KEY"] = "AIzaSyADaLOm5yZT5k0xGGmPpltn_Q-YdhPBZM4"
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3)

@tool
def generate_pitch_script(input_text: str) -> str:
    """Generate a full pitch script from structure and persona info."""
    prompt = f"""
You are a Pitch Script Generator Agent.

Input: {input_text}

Create a script with:
- Opening Hook
- Customer Pain
- Value Proposition
- Product Solution
- Call to Action

Return plain text only. No markdown, no explanations.
"""
    response = llm.invoke(prompt)
    return response.content.strip()

tools = [generate_pitch_script]
agent = initialize_agent(tools=tools, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.tools import tool

os.environ["GOOGLE_API_KEY"] = "AIzaSyBa1JwyAJR92hZNM_tgbF5qVkXZLBeGRqE"
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3)

@tool
def refine_pitch_with_feedback(input_text: str) -> str:
    """Refine pitch using feedback. Return updated script, summary, and changes."""
    prompt = f"""
You are a Feedback-Driven Refiner Agent.

Input: {input_text}

Return output with 3 labeled sections:
- Feedback Summary
- Changes Applied
- Refined Pitch Script

Do not include markdown or formatting. Plain text only.
"""
    response = llm.invoke(prompt)
    return response.content.strip()

tools = [refine_pitch_with_feedback]
agent = initialize_agent(tools=tools, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)



import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.tools import tool

os.environ["GOOGLE_API_KEY"] = "AIzaSyCJeinQODD5WZwpsAZS12qDiwlSmRaE1Mk"
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3)

@tool
def compose_pitch_structure(input_text: str) -> str:
    """Compose a structured pitch layout in 5 parts based on user input."""
    prompt = f"""
You are a Pitch Structure Composer Agent.

Input: {input_text}

Return JSON with 5 sections:
- Identify Need
- Evaluate Alternatives
- Present Fit
- Offer Benefits
- Align with Market

Only return valid JSON. No markdown or text outside the object.
"""
    response = llm.invoke(prompt)
    try:
        content = response.content.strip().strip('`').strip()
        return json.dumps(json.loads(content), indent=2)
    except Exception as e:
        return f"⚠️ JSON Parse Error: {e}\nRaw: {response.content}"

tools = [compose_pitch_structure]
agent = initialize_agent(tools=tools, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

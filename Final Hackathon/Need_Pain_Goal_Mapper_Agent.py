import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.tools import tool

os.environ["GOOGLE_API_KEY"] = "AIzaSyB-uX72nApl_-GWcjBQizuGrO4n7679sHg"
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3)

@tool
def map_need_to_pain_and_goal(input_text: str) -> str:
    """Map user needs to goals, pain points, and success criteria in JSON format."""
    prompt = f"""
You are a Need-Pain-Goal Mapper Agent.

Input: {input_text}

Output JSON must include:
- Goals
- Pain Points
- Decision Points
- Success Criteria
- Themes (Functional, Emotional, Social)

Only return valid JSON. No markdown or extra text.
"""
    response = llm.invoke(prompt)
    try:
        content = response.content.strip().strip('`').strip()
        return json.dumps(json.loads(content), indent=2)
    except Exception as e:
        return f"⚠️ JSON Parse Error: {e}\nRaw: {response.content}"

tools = [map_need_to_pain_and_goal]
agent = initialize_agent(tools=tools, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

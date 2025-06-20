import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.tools import tool

os.environ["GOOGLE_API_KEY"] = "AIzaSyCuTGErckZCgI_kH2VcsJPyhHHz0MEJSU8"
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3)

@tool
def extract_user_needs(input_text: str) -> str:
    """Extract user needs, environment, and influences in JSON format."""
    prompt = f"""
You are a User Research Extractor Agent.
Given user feedback, output JSON with:
- "Need"
- "Environment"
- "Influences"

Feedback:
{input_text}

Return only valid JSON. Do not include markdown or explanations.
"""
    response = llm.invoke(prompt)
    try:
        content = response.content.strip().strip('`').strip()
        return json.dumps(json.loads(content), indent=2)
    except Exception as e:
        return f"⚠️ JSON Parse Error: {e}\nRaw: {response.content}"

tools = [extract_user_needs]
agent = initialize_agent(tools=tools, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

import os
from langchain.llms import Together
from langchain.agents import load_tools, initialize_agent, AgentType
from dotenv import load_dotenv

load_dotenv()

def simulate_personality(data):
    llm = Together(
        model="mistralai/Mistral-7B-Instruct-v0.1",
        temperature=0.5,
        max_tokens=300,
        together_api_key=os.getenv("TOGETHER_API_KEY")
    )

    tools = load_tools(["wikipedia"], llm=llm)

    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=False)

    prompt = f"""Given the following founder attributes, generate a personality profile:

MBTI: {data['mbti']}
Core Values: {data['values']}
Risk Appetite: {data['risk']}
Communication Style: {data['comm']}
Decision Speed: {data['decision']}
Conflict Style: {data['conflict']}

Output a concise behavioral summary."""
    
    return agent.run(prompt)

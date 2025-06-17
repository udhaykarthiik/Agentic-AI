import os
from langchain.llms import Together
from langchain.agents import load_tools, initialize_agent, AgentType
from dotenv import load_dotenv

load_dotenv()

def simulate_debate(profile1, profile2):
    llm = Together(
        model="mistralai/Mistral-7B-Instruct-v0.1",
        temperature=0.7,
        max_tokens=400,
        together_api_key=os.getenv("TOGETHER_API_KEY")
    )

    tools = load_tools(["wikipedia"], llm=llm)

    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=False)

    prompt = f"""Two founders are collaborating on a startup.

Founder 1 Profile:
{profile1}

Founder 2 Profile:
{profile2}

Simulate a discussion between them on this scenario:
"Should we raise funding now or bootstrap longer?"

Return:
1. Founder 1 opinion
2. Founder 2 opinion
3. Final decision or likely tension point"""
    
    return agent.run(prompt)

import os
from langchain.llms import Together
from langchain.agents import load_tools, initialize_agent, AgentType
from dotenv import load_dotenv

load_dotenv()

def conflict_agent(profiles_combined, debate_summary):
    llm = Together(
        model="mistralai/Mistral-7B-Instruct-v0.1",
        temperature=0.6,
        max_tokens=400,
        together_api_key=os.getenv("TOGETHER_API_KEY")
    )

    tools = load_tools(["wikipedia"], llm=llm)

    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=False)

    prompt = f"""Based on the founders' combined personality summaries and their scenario debate, identify:

1. Potential personality clashes
2. Misalignment in values or styles
3. Advice for conflict prevention

Founder Profiles:
{profiles_combined}

Debate Summary:
{debate_summary}

Output in markdown."""
    
    return agent.run(prompt)

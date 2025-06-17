import os
from langchain.llms import Together

# ✅ Set Together API Key
os.environ["TOGETHER_API_KEY"] = "988d73e388e1b6c2e5c4b1517b2a07f4c21dd8d9b48f585da410cc6094a6c6d4"

# ✅ Initialize LLM
llm = Together(
    model="togethercomputer/llama-2-70b-chat",
    temperature=0.7,
    max_tokens=512
)

def simulate_scenario(input_text: str) -> str:
    """Simulate a typical startup decision-making scenario between two founders."""
    prompt = f"Simulate founder conflict scenario: {input_text}"
    return llm.invoke(prompt)

import gradio as gr
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnableSequence
from typing import Dict, Any

# Initialize the LLM (Gemini 1.5 Flash)
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key="AIzaSyD8bmDKJZsWH19pKjapzXFIXEN_sGxrAxc"  # Replace with your actual Gemini API key
)

# MBTI explanation for users unfamiliar with MBTI
MBTI_INFO = """
**What is MBTI?**
The Myers-Briggs Type Indicator (MBTI) is a personality framework that categorizes people into 16 types based on four dichotomies: 
- **Introversion (I) vs. Extraversion (E)**: How you gain energy (inward vs. outward).
- **Sensing (S) vs. Intuition (N)**: How you process information (facts vs. possibilities).
- **Thinking (T) vs. Feeling (F)**: How you make decisions (logic vs. values).
- **Judging (J) vs. Perceiving (P)**: How you approach structure (organized vs. flexible).

**Examples**:
- **INTJ**: Strategic, independent thinkers who plan long-term (e.g., 'The Mastermind').
- **ENTP**: Creative, quick-witted debaters who love new ideas (e.g., 'The Visionary').
- **INFJ**: Empathetic, insightful idealists (e.g., 'The Advocate').
- **ESTJ**: Organized, practical leaders (e.g., 'The Executive').

For more details, visit [16Personalities](https://www.16personalities.com/) to take a free test or learn about your type.
"""

# Define functions for the simulation
def simulate_personality(input_data: Dict[str, Any]) -> str:
    """Simulate a co-founder's behavior based on extended inputs."""
    if not isinstance(input_data, dict):
        raise ValueError(f"Expected dict input, got {type(input_data)}")

    prompt = PromptTemplate.from_template("""
        You are a co-founder with:
        - MBTI type: {mbti}
        - Core values: {values}
        - Risk appetite: {risk_appetite}/10
        - Communication style: {comm_style}
        - Decision-making speed: {decision_speed}
        - Conflict resolution approach: {conflict_approach}
        Describe how you would approach decision-making in a startup, integrating all these traits.
        Highlight how your communication style, decision speed, and conflict approach influence your behavior.
        Provide a detailed profile in 150-200 words.
    """)
    chain = RunnableSequence(prompt | llm)
    response = chain.invoke({
        "mbti": input_data.get("mbti", "Unsure"),
        "values": input_data.get("values", ""),
        "risk_appetite": input_data.get("risk_appetite", 5),
        "comm_style": input_data.get("comm_style", "Direct"),
        "decision_speed": input_data.get("decision_speed", "Balanced"),
        "conflict_approach": input_data.get("conflict_approach", "Collaborative")
    })
    return response.content

def simulate_debate(founder1_profile: str, founder2_profile: str, scenario: str) -> str:
    """Simulate a debate between two co-founders on a given scenario."""
    prompt = PromptTemplate.from_template("""
        Founder 1: {founder1_profile}
        Founder 2: {founder2_profile}
        Scenario: {scenario}
        Simulate a debate between the two founders on the given scenario. Highlight how their MBTI, values, risk appetite,
        communication styles, decision-making speeds, and conflict resolution approaches shape their arguments.
        Identify areas of agreement, disagreement, and specific tension points. Output a summary (200-250 words)
        of the debate, including key arguments and tension points.
    """)
    chain = RunnableSequence(prompt | llm)
    response = chain.invoke({
        "founder1_profile": founder1_profile,
        "founder2_profile": founder2_profile,
        "scenario": scenario
    })
    return response.content

def analyze_alignment(debate_summary: str) -> str:
    """Analyze alignment and suggest agreements/division of responsibilities."""
    prompt = PromptTemplate.from_template("""
        Based on the debate summary: {debate_summary}
        1. Calculate an alignment score (0-100) based on the level of agreement between the founders.
        2. Identify specific tension points, considering MBTI, values, risk appetite, communication styles,
           decision-making speeds, and conflict resolution approaches.
        3. Suggest a detailed founder agreement to address these tensions.
        4. Propose a division of responsibilities to leverage strengths and minimize conflicts.
        Output the response in the following format:
        - **Alignment Score**: [Score]
        - **Tension Points**: [List of tension points]
        - **Suggested Founder Agreement**: [Agreement details]
        - **Division of Responsibilities**: [Role assignments]
    """)
    chain = RunnableSequence(prompt | llm)
    response = chain.invoke({"debate_summary": debate_summary})
    return response.content

# Gradio interface
def run_simulation(founder1_mbti, founder1_values, founder1_risk, founder1_comm_style, founder1_decision_speed, founder1_conflict_approach,
                   founder2_mbti, founder2_values, founder2_risk, founder2_comm_style, founder2_decision_speed, founder2_conflict_approach):
    try:
        # Validate inputs
        if not founder1_values or not founder2_values:
            return "Error: Please provide core values for both founders."
        if not all([founder1_mbti, founder1_comm_style, founder1_decision_speed, founder1_conflict_approach,
                    founder2_mbti, founder2_comm_style, founder2_decision_speed, founder2_conflict_approach]):
            return "Error: Please fill in all dropdown fields for both founders."

        # Step 1: Simulate personalities
        founder1_input = {
            "mbti": founder1_mbti,
            "values": founder1_values,
            "risk_appetite": founder1_risk,
            "comm_style": founder1_comm_style,
            "decision_speed": founder1_decision_speed,
            "conflict_approach": founder1_conflict_approach
        }
        founder2_input = {
            "mbti": founder2_mbti,
            "values": founder2_values,
            "risk_appetite": founder2_risk,
            "comm_style": founder2_comm_style,
            "decision_speed": founder2_decision_speed,
            "conflict_approach": founder2_conflict_approach
        }
        
        founder1_profile = simulate_personality(founder1_input)
        founder2_profile = simulate_personality(founder2_input)

        # Step 2: Simulate debates for three scenarios
        scenarios = ["Pivot vs. Persevere", "Raise Funding Now vs. Later", "Hire Team Now vs. Bootstrap"]
        debate_results = []
        for scenario in scenarios:
            debate = simulate_debate(founder1_profile, founder2_profile, scenario)
            debate_results.append(f"### {scenario}\n{debate}")

        # Step 3: Analyze alignment
        combined_debates = "\n".join(debate_results)
        analysis = analyze_alignment(combined_debates)

        # Return results
        return f"""
        ## Founder Profiles
        ### Founder 1
        {founder1_profile}
        ### Founder 2
        {founder2_profile}
        ## Debate Summaries
        {combined_debates}
        ## Analysis
        {analysis}
        """
    except Exception as e:
        return f"Error: {str(e)}"

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# Co-Founder Personality Clash Detector")
    gr.Markdown("Enter details for two co-founders to simulate their dynamics and assess compatibility.")
    
    with gr.Accordion("What is MBTI? (Click to learn more)", open=False):
        gr.Markdown(MBTI_INFO)
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### Founder 1")
            founder1_mbti = gr.Dropdown(
                label="MBTI Type (Select 'Unsure' if unknown)",
                choices=["INTJ", "ENTP", "INFJ", "ESTJ", "Other", "Unsure"],
                value="INTJ"
            )
            founder1_values = gr.Textbox(
                label="Core Values (e.g., Innovation, Stability, Teamwork)",
                placeholder="Enter values, separated by commas"
            )
            founder1_risk = gr.Slider(
                label="Risk Appetite (1 = Low, 10 = High)",
                minimum=1,
                maximum=10,
                step=1,
                value=5
            )
            founder1_comm_style = gr.Dropdown(
                label="Communication Style",
                choices=["Direct", "Diplomatic", "Collaborative", "Reserved"],
                value="Direct"
            )
            founder1_decision_speed = gr.Dropdown(
                label="Decision-Making Speed",
                choices=["Quick", "Deliberate", "Balanced"],
                value="Balanced"
            )
            founder1_conflict_approach = gr.Dropdown(
                label="Conflict Resolution Approach",
                choices=["Collaborative", "Competitive", "Avoidant", "Compromising"],
                value="Collaborative"
            )
        
        with gr.Column():
            gr.Markdown("### Founder 2")
            founder2_mbti = gr.Dropdown(
                label="MBTI Type (Select 'Unsure' if unknown)",
                choices=["INTJ", "ENTP", "INFJ", "ESTJ", "Other", "Unsure"],
                value="ENTP"
            )
            founder2_values = gr.Textbox(
                label="Core Values (e.g., Innovation, Stability, Teamwork)",
                placeholder="Enter values, separated by commas"
            )
            founder2_risk = gr.Slider(
                label="Risk Appetite (1 = Low, 10 = High)",
                minimum=1,
                maximum=10,
                step=1,
                value=5
            )
            founder2_comm_style = gr.Dropdown(
                label="Communication Style",
                choices=["Direct", "Diplomatic", "Collaborative", "Reserved"],
                value="Direct"
            )
            founder2_decision_speed = gr.Dropdown(
                label="Decision-Making Speed",
                choices=["Quick", "Deliberate", "Balanced"],
                value="Balanced"
            )
            founder2_conflict_approach = gr.Dropdown(
                label="Conflict Resolution Approach",
                choices=["Collaborative", "Competitive", "Avoidant", "Compromising"],
                value="Collaborative"
            )
    
    submit_btn = gr.Button("Run Simulation")
    output = gr.Markdown(label="Results")
    
    submit_btn.click(
        fn=run_simulation,
        inputs=[
            founder1_mbti, founder1_values, founder1_risk, founder1_comm_style, founder1_decision_speed, founder1_conflict_approach,
            founder2_mbti, founder2_values, founder2_risk, founder2_comm_style, founder2_decision_speed, founder2_conflict_approach
        ],
        outputs=output
    )

demo.launch()
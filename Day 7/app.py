import gradio as gr
from agents.simulate_personality import simulate_personality
from agents.simulate_debate import simulate_debate
from agents.conflict_agent import conflict_agent

# MBTI explanation for UI
MBTI_INFO = """
**What is MBTI?**
The Myers-Briggs Type Indicator (MBTI) is a personality framework that categorizes people into 16 types based on four dichotomies: 
- **Introversion (I) vs. Extraversion (E)**: How you gain energy (inward vs. outward).
- **Sensing (S) vs. Intuition (N)**: How you process information (facts vs. possibilities).
- **Thinking (T) vs. Feeling (F)**: How you make decisions (logic vs. values).
- **Judging (J) vs. Perceiving (P)**: How you approach structure (organized vs. flexible).

Examples:
- **INTJ**: Strategic, independent thinkers who plan long-term.
- **ENTP**: Creative, quick-witted debaters who love new ideas.
- **INFJ**: Empathetic, insightful idealists.
- **ESTJ**: Organized, practical leaders.
"""

def run_simulation(
    mbti1, values1, risk1, comm1, speed1, conflict1,
    mbti2, values2, risk2, comm2, speed2, conflict2
):
    try:
        if not values1 or not values2:
            return "❌ Please provide core values for both founders."

        # Founder 1 personality
        profile1 = simulate_personality({
            "mbti": mbti1, "values": values1, "risk": risk1,
            "comm": comm1, "decision": speed1, "conflict": conflict1
        })

        # Founder 2 personality
        profile2 = simulate_personality({
            "mbti": mbti2, "values": values2, "risk": risk2,
            "comm": comm2, "decision": speed2, "conflict": conflict2
        })

        # Debate simulation
        debate = simulate_debate(profile1, profile2)

        # Conflict analysis
        alignment = conflict_agent(profile1 + "\n\n" + profile2, debate)

        return f"""
## 🧠 Founder Profiles
### Founder 1
{profile1}

### Founder 2
{profile2}

---

## 💬 Debate Simulation
{debate}

---

## ⚖️ Conflict Analysis & Suggestions
{alignment}
"""

    except Exception as e:
        return f"❗ Error occurred: {str(e)}"


# ---------- Gradio UI ----------
with gr.Blocks() as demo:
    gr.Markdown("# 🤝 Co-Founder Personality Clash Detector")
    gr.Markdown("Enter the personality details of both founders and simulate alignment, debate, and conflict risks.")

    with gr.Accordion("What is MBTI?", open=False):
        gr.Markdown(MBTI_INFO)

    with gr.Row():
        with gr.Column():
            gr.Markdown("### 🧑 Founder 1")
            mbti1 = gr.Dropdown(label="MBTI Type", choices=["INTJ", "ENTP", "INFJ", "ESTJ", "Other", "Unsure"], value="INTJ")
            values1 = gr.Textbox(label="Core Values (comma-separated)", placeholder="e.g., Innovation, Integrity, Teamwork")
            risk1 = gr.Slider(label="Risk Appetite (1-10)", minimum=1, maximum=10, value=5)
            comm1 = gr.Dropdown(label="Communication Style", choices=["Direct", "Diplomatic", "Collaborative", "Reserved"], value="Direct")
            speed1 = gr.Dropdown(label="Decision-Making Speed", choices=["Quick", "Deliberate", "Balanced"], value="Balanced")
            conflict1 = gr.Dropdown(label="Conflict Resolution", choices=["Collaborative", "Competitive", "Avoidant", "Compromising"], value="Collaborative")

        with gr.Column():
            gr.Markdown("### 👨‍💼 Founder 2")
            mbti2 = gr.Dropdown(label="MBTI Type", choices=["INTJ", "ENTP", "INFJ", "ESTJ", "Other", "Unsure"], value="ENTP")
            values2 = gr.Textbox(label="Core Values (comma-separated)", placeholder="e.g., Innovation, Integrity, Teamwork")
            risk2 = gr.Slider(label="Risk Appetite (1-10)", minimum=1, maximum=10, value=5)
            comm2 = gr.Dropdown(label="Communication Style", choices=["Direct", "Diplomatic", "Collaborative", "Reserved"], value="Direct")
            speed2 = gr.Dropdown(label="Decision-Making Speed", choices=["Quick", "Deliberate", "Balanced"], value="Balanced")
            conflict2 = gr.Dropdown(label="Conflict Resolution", choices=["Collaborative", "Competitive", "Avoidant", "Compromising"], value="Collaborative")

    submit = gr.Button("🔍 Run Simulation")
    output = gr.Markdown()

    submit.click(
        fn=run_simulation,
        inputs=[mbti1, values1, risk1, comm1, speed1, conflict1,
                mbti2, values2, risk2, comm2, speed2, conflict2],
        outputs=output
    )

demo.launch()

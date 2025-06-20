import streamlit as st
import json
from agents.User_Research_Extractor_Agent import agent as user_research_agent
from agents.Need_Pain_Goal_Mapper_Agent import agent as need_pain_goal_agent
from agents.Pitch_Structure_Composer_Agent import agent as pitch_structure_agent
from agents.Pitch_Script_Generator_Agent import agent as pitch_script_agent
from agents.Feedback_Driven_Refiner_Agent import agent as feedback_refiner_agent

st.set_page_config(page_title="Agentic AI Pitch Builder", layout="wide")

# 🌙 Dark mode toggle
dark_mode = st.sidebar.toggle("🌙 Dark Mode", value=False)

# 🎨 Inject CSS
st.markdown(f"""
    <style>
    body {{
        background-color: {'#0e1117' if dark_mode else '#f8f9fa'};
        color: {'#f1f1f1' if dark_mode else '#202124'};
    }}
    .main {{ background-color: inherit; }}
    h1, h2, h3 {{
        color: {'#ffffff' if dark_mode else '#202124'};
        font-family: 'Segoe UI', sans-serif;
    }}
    .stTextArea textarea {{
        border-radius: 10px !important;
        border: 1px solid {'#444' if dark_mode else '#ccc'} !important;
        padding: 0.75rem;
        font-size: 15px;
        background-color: {'#1e1e1e' if dark_mode else '#ffffff'};
        color: {'#ffffff' if dark_mode else '#000000'};
    }}
    .stButton > button {{
        background-color: #ff4b4b;
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        margin-top: 10px;
    }}
    .stTabs [role="tab"] {{
        background: {'#333333' if dark_mode else '#e6e6e6'};
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        margin-right: 5px;
    }}
    .stTabs [aria-selected="true"] {{
        background: #ff4b4b;
        color: white;
    }}
    </style>
""", unsafe_allow_html=True)

# 🔥 App title
st.title("🎯 Agentic AI Sales Pitch Generator")
st.markdown("Craft compelling, structured pitches step-by-step using AI agents.")

# 🧠 Helper function to render output
def try_show_json(response):
    try:
        if response.strip().startswith("```"):
            response = response.strip().split("```")[1]
        st.json(json.loads(response))
    except Exception:
        st.text(response)

# 🧩 Tab layout for agents
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "1️⃣ Extract User Needs",
    "2️⃣ Map Needs to Goals",
    "3️⃣ Compose Pitch Structure",
    "4️⃣ Generate Pitch Script",
    "5️⃣ Refine with Feedback"
])

# Agent 1
with tab1:
    st.subheader("🧠 Agent 1: User Research Extractor")
    with st.expander("✏️ Input User Feedback"):
        user_feedback = st.text_area("Enter raw user feedback or survey notes", height=150)
    if st.button("Run Agent 1"):
        with st.spinner("Analyzing feedback..."):
            result = user_research_agent.run(user_feedback)
            st.success("✅ User Needs Extracted")
            try_show_json(result)

# Agent 2
with tab2:
    st.subheader("🔍 Agent 2: Need-Pain-Goal Mapper")
    with st.expander("📥 Paste Output from Agent 1"):
        step1_output = st.text_area("Agent 1 Output JSON", height=200)
    if st.button("Run Agent 2"):
        with st.spinner("Mapping pain points and goals..."):
            result = need_pain_goal_agent.run(step1_output)
            st.success("✅ Mapping Complete")
            try_show_json(result)

# Agent 3
with tab3:
    st.subheader("🏗️ Agent 3: Pitch Structure Composer")
    with st.expander("📥 Paste Mapped Needs + Project Info"):
        combined_input = st.text_area("Combine Agent 2 output + project description", height=250)
    if st.button("Run Agent 3"):
        with st.spinner("Composing pitch structure..."):
            result = pitch_structure_agent.run(combined_input)
            st.success("✅ Pitch Structure Created")
            try_show_json(result)

# Agent 4
with tab4:
    st.subheader("📝 Agent 4: Pitch Script Generator")
    with st.expander("📥 Paste Pitch Structure & Persona Info"):
        pitch_script_input = st.text_area("Pitch structure + persona", height=250)
    if st.button("Run Agent 4"):
        with st.spinner("Generating pitch script..."):
            result = pitch_script_agent.run(pitch_script_input)
            st.success("✅ Script Generated")
            st.text(result)

# Agent 5
with tab5:
    st.subheader("🔧 Agent 5: Feedback-Driven Refiner")
    with st.expander("📥 Paste Script & Feedback"):
        feedback_input = st.text_area("Enter pitch script + feedback", height=250)
    if st.button("Run Agent 5"):
        with st.spinner("Refining pitch..."):
            result = feedback_refiner_agent.run(feedback_input)
            st.success("✅ Script Refined")
            st.text(result)

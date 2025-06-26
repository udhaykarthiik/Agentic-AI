import streamlit as st
import os
import sqlite3
from datetime import datetime
import uuid
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import BaseTool
import re

# Custom Tool Class for CrewAI
class TextProcessorTool(BaseTool):
    name: str = "Text Processor Tool"
    description: str = "Processes input text by converting to uppercase and counting words."

    def _run(self, input_text: str) -> dict:
        return {"processed_text": input_text.upper(), "word_count": len(input_text.split())}

# Configure Google Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBPVAaH8FHNady3yzEuRpAz-92Fa_b1Qvo")
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY  # Set for litellm
gemini_llm = LLM(model="gemini/gemini-2.0-flash", api_key=GEMINI_API_KEY)

# SQLite Database Setup
def init_db():
    conn = sqlite3.connect("sales_pitch.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS projects (
        id TEXT PRIMARY KEY,
        details TEXT,
        created_at TIMESTAMP
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS need_models (
        id TEXT PRIMARY KEY,
        project_id TEXT,
        user_needs TEXT,
        created_at TIMESTAMP
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS pitch_scripts (
        id TEXT PRIMARY KEY,
        project_id TEXT,
        structure TEXT,
        script TEXT,
        created_at TIMESTAMP
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS feedback (
        id TEXT PRIMARY KEY,
        project_id TEXT,
        feedback TEXT,
        refined_script TEXT,
        created_at TIMESTAMP
    )''')
    conn.commit()
    conn.close()

init_db()

# CrewAI Agents
manager_agent = Agent(
    role="Manager",
    goal="Oversee and coordinate the sales pitch generation process",
    backstory="Experienced project manager skilled in orchestrating multi-agent workflows for optimal efficiency.",
    llm=gemini_llm,
    tools=[TextProcessorTool()],
    verbose=True
)

user_research_agent = Agent(
    role="User Research Extractor",
    goal="Extract user needs from feedback, voice notes, or surveys",
    backstory="Expert in synthesizing user behavior, environment, and goals from diverse inputs.",
    llm=gemini_llm,
    tools=[TextProcessorTool()],
    verbose=True
)

need_pain_goal_agent = Agent(
    role="Need-Pain-Goal Mapper",
    goal="Map user needs to pain points and goals using jobs-to-be-done framework",
    backstory="Skilled in transforming raw feedback into actionable insights for targeted solutions.",
    llm=gemini_llm,
    tools=[TextProcessorTool()],
    verbose=True
)

pitch_structure_agent = Agent(
    role="Pitch Structure Composer",
    goal="Design a modular pitch structure based on user needs and project details",
    backstory="Specialist in creating persuasive, structured pitch frameworks tailored to audience needs.",
    llm=gemini_llm,
    tools=[TextProcessorTool()],
    verbose=True
)

pitch_script_agent = Agent(
    role="Pitch Script Generator",
    goal="Generate a customized sales pitch script for the target persona",
    backstory="Expert in crafting empathetic, persuasive, and concise sales scripts for diverse audiences.",
    llm=gemini_llm,
    tools=[TextProcessorTool()],
    verbose=True
)

feedback_refiner_agent = Agent(
    role="Feedback-Driven Refiner",
    goal="Refine pitch scripts based on peer or mentor feedback",
    backstory="Proficient in analyzing feedback and iteratively improving pitch quality for maximum impact.",
    llm=gemini_llm,
    tools=[TextProcessorTool()],
    verbose=True
)

# CrewAI Tasks
def create_tasks(project_details, feedback_data, persona):
    manager_task = Task(
        description=f"Oversee the sales pitch generation process. Coordinate inputs: project details ({project_details}), feedback ({feedback_data}), and persona ({persona}). Provide a plain text confirmation of coordination and oversight.",
        agent=manager_agent,
        expected_output="Plain text confirmation of task coordination and oversight"
    )

    user_research_task = Task(
        description=f"Extract user needs from feedback: {feedback_data}. Use the Text Processor Tool to analyze input. Output a plain text summary of user needs and influences, formatted as a bulleted list (e.g., '- Need: Task management, Influences: Time constraints').",
        agent=user_research_agent,
        expected_output="Plain text summary of user needs and influences as a bulleted list"
    )

    need_pain_goal_task = Task(
        description="Map user needs to pain points and goals using jobs-to-be-done framework. Input: User need model. Use the Text Processor Tool to cluster themes. Output a plain text summary with goals, pain points, and themes (functional, emotional, social), formatted with clear sections (e.g., 'Goals:\n- ...', 'Pain Points:\n- ...').",
        agent=need_pain_goal_agent,
        expected_output="Plain text summary of goals, pain points, and themes with sections"
    )

    pitch_structure_task = Task(
        description=f"Design pitch structure using project details: {project_details} and user needs. Use the Text Processor Tool to validate structure. Include sections: Identify Need, Evaluate Alternatives, Present Fit, Offer Benefits, Align with Market. Output a plain text description of the pitch structure, formatted with numbered sections (e.g., '1. Identify Need: ...').",
        agent=pitch_structure_agent,
        expected_output="Plain text description of pitch structure with numbered sections"
    )

    pitch_script_task = Task(
        description=f"Generate a pitch script under 300 words for persona: {persona}. Input: Pitch structure. Use the Text Processor Tool to ensure conciseness. Output a plain text pitch script with labeled sections (e.g., 'Opening Hook: ...', 'Customer Pain: ...', 'Value Prop: ...', 'Product Solution: ...', 'CTA: ...').",
        agent=pitch_script_agent,
        expected_output="Plain text pitch script with labeled sections"
    )

    feedback_refiner_task = Task(
        description=f"Refine pitch script based on feedback: {feedback_data}. Use the Text Processor Tool to summarize feedback. Output a plain text summary of the feedback and the refined pitch script, formatted with sections (e.g., 'Feedback Summary:\n...\nRefined Pitch Script:\n- Opening Hook: ...').",
        agent=feedback_refiner_agent,
        expected_output="Plain text summary of feedback and refined pitch script with sections"
    )

    return [manager_task, user_research_task, need_pain_goal_task, pitch_structure_task, pitch_script_task, feedback_refiner_task]

# Function to strip markdown code blocks
def strip_markdown(text: str) -> str:
    # Remove ```json ... ``` or ``` ... ``` code blocks
    return re.sub(r'```(?:json)?\s*([\s\S]*?)\s*```', r'\1', text).strip()

# Streamlit UI
st.title("Sales Pitch Generator")

# Custom CSS for styled headings
st.markdown("""
    <style>
    .section-heading {
        font-size: 1.5em;
        font-weight: bold;
        color: #2E2E2E;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .text-box {
        border: 1px solid #CCCCCC;
        border-radius: 5px;
        padding: 10px;
        background-color: #F9F9F9;
        min-height: 100px;
    }
    </style>
""", unsafe_allow_html=True)

with st.form("pitch_form"):
    project_details = st.text_area("Project Details", height=150)
    feedback_data = st.text_area("User Feedback/Surveys", height=150)
    persona = st.text_input("Target Persona (e.g., student, educator)")
    submitted = st.form_submit_button("Generate Pitch")

if submitted:
    if not project_details or not feedback_data or not persona:
        st.error("Please fill in all fields.")
    else:
        # Generate unique project ID
        project_id = str(uuid.uuid4())

        # Save project details to database
        conn = sqlite3.connect("sales_pitch.db")
        c = conn.cursor()
        c.execute("INSERT INTO projects (id, details, created_at) VALUES (?, ?, ?)",
                  (project_id, project_details, datetime.now()))
        conn.commit()
        conn.close()

        # Run CrewAI workflow
        with st.spinner("Generating pitch..."):
            tasks = create_tasks(project_details, feedback_data, persona)
            crew = Crew(
                agents=[manager_agent, user_research_agent, need_pain_goal_agent, pitch_structure_agent, pitch_script_agent, feedback_refiner_agent],
                tasks=tasks,
                process=Process.sequential,
                verbose=True
            )
            try:
                result = crew.kickoff()
                st.write("CrewAI execution completed successfully.")
            except Exception as e:
                st.error(f"Error during CrewAI execution: {e}")
                st.stop()

            # Process task outputs
            outputs = {}
            for i, task_name in enumerate(["manager", "user_research", "need_pain_goal", "pitch_structure", "pitch_script", "feedback_refiner"]):
                try:
                    output = tasks[i].output
                    if hasattr(output, "raw") and isinstance(output.raw, str):
                        # Strip markdown code blocks and treat as plain text
                        outputs[task_name] = strip_markdown(output.raw)
                    else:
                        st.warning(f"Task {task_name} output is not a valid string: {output}")
                        outputs[task_name] = f"Error: Invalid output format for task {task_name}"
                except Exception as e:
                    st.warning(f"Error processing output for task {task_name}: {e}")
                    outputs[task_name] = f"Error: Output processing failed: {e}"

            # Save results to database
            conn = sqlite3.connect("sales_pitch.db")
            c = conn.cursor()
            try:
                if "user_research" in outputs and not outputs["user_research"].startswith("Error"):
                    c.execute("INSERT INTO need_models (id, project_id, user_needs, created_at) VALUES (?, ?, ?, ?)",
                              (str(uuid.uuid4()), project_id, outputs["user_research"], datetime.now()))
                if "pitch_structure" in outputs and "pitch_script" in outputs and not outputs["pitch_script"].startswith("Error"):
                    c.execute("INSERT INTO pitch_scripts (id, project_id, structure, script, created_at) VALUES (?, ?, ?, ?, ?)",
                              (str(uuid.uuid4()), project_id, outputs["pitch_structure"], outputs["pitch_script"], datetime.now()))
                if "feedback_refiner" in outputs and not outputs["feedback_refiner"].startswith("Error"):
                    c.execute("INSERT INTO feedback (id, project_id, feedback, refined_script, created_at) VALUES (?, ?, ?, ?, ?)",
                              (str(uuid.uuid4()), project_id, feedback_data, outputs["feedback_refiner"], datetime.now()))
                conn.commit()
            except Exception as e:
                st.error(f"Error saving to database: {e}")
            finally:
                conn.close()

            # Display results in styled text boxes
            st.markdown('<div class="section-heading">User Need Model</div>', unsafe_allow_html=True)
            if "user_research" in outputs and not outputs["user_research"].startswith("Error"):
                st.text_area("", value=outputs["user_research"], height=150, disabled=True, key="user_need_model")
            else:
                st.warning("No user need model output available.")

            st.markdown('<div class="section-heading">Pitch Script</div>', unsafe_allow_html=True)
            if "pitch_script" in outputs and not outputs["pitch_script"].startswith("Error"):
                st.text_area("", value=outputs["pitch_script"], height=200, disabled=True, key="pitch_script")
            else:
                st.warning("No pitch script output available.")

            st.markdown('<div class="section-heading">Refined Script</div>', unsafe_allow_html=True)
            if "feedback_refiner" in outputs and not outputs["feedback_refiner"].startswith("Error"):
                # Split feedback summary and refined pitch script for better formatting
                feedback_parts = outputs["feedback_refiner"].split("Refined Pitch Script:", 1)
                feedback_summary = feedback_parts[0].strip()
                refined_script = feedback_parts[1].strip() if len(feedback_parts) > 1 else "No refined script provided."
                formatted_output = f"Feedback Summary:\n{feedback_summary}\n\nRefined Pitch Script:\n{refined_script}"
                st.text_area("", value=formatted_output, height=300, disabled=True, key="refined_script")
            else:
                st.warning("No refined script output available.")

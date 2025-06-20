# 🤖 Agentic Sales Pitch Generator

An intelligent, multi-agent system that helps startups and founders automatically generate well-structured, personalized sales pitches using AI.

## 🔴 Problem Statement
Founders often struggle to explain their ideas clearly to investors or customers. Traditional pitch writing is time-consuming and lacks structure, especially for early-stage startups.

## 🎯 Solution
We built a 5-agent AI system using LangChain and Gemini models that takes in user feedback and project descriptions and turns them into a polished 300-word sales pitch — with clear steps and refinement built-in.

## 🧠 Flow Overview

1. **User Input**  
   Project description and raw user feedback.

2. **Agent 1: User Research Extractor**  
   Extracts user needs in structured format:  
   `→ Need`, `→ Environment`, `→ Influences`

3. **Agent 2: Need-Pain-Goal Mapper**  
   Maps needs into:  
   `→ Goals`, `→ Pain Points`, `→ Success Criteria`, `→ Themes`

4. **Agent 3: Pitch Structure Composer**  
   Generates 5-part pitch structure:  
   `→ Identify Need`, `→ Alternatives`, `→ Fit`, `→ Benefits`, `→ Market Alignment`

5. **Agent 4: Pitch Script Generator**  
   Converts structure into full pitch with:
   `→ Hook`, `→ Pain`, `→ Solution`, `→ Value`, `→ CTA`

6. **Agent 5: Feedback Refiner**  
   Takes feedback and rewrites/refines the script.

## ✅ Final Output
A clean, persuasive, 300-word pitch tailored to a target persona, ready to present to investors, accelerators, or users.

## 🛠️ Tech Stack

- [x] **Streamlit** (Frontend UI with tabs and dark mode)
- [x] **LangChain Agents**
- [x] **Google Gemini LLM (via langchain-google-genai)**
- [x] CSS styled flow and JSON-safe output
- [x] Modular structure with reusable Python agent files

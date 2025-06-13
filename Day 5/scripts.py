import os
import PyPDF2
import gradio as gr
import google.generativeai as genai

# 🔐 Set your Gemini API Key
GEMINI_API_KEY = "AIzaSyDCPZvnagJobQ4Ne-a3XGKXjPHn5uD42gw"  # Replace with your actual key
genai.configure(api_key=GEMINI_API_KEY)

# 📄 Extract text from PDF
def extract_pdf_text(file):
    text = ""
    reader = PyPDF2.PdfReader(file)
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

# ✂️ Summarize content
def summarize_content(content):
    prompt = f"""
    Summarize the following study material into 3–5 bullet points:

    \"\"\"{content}\"\"\"
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()

# 📝 Generate MCQs
def generate_mcqs_from_summary(summary):
    prompt = f"""
    Based on the following summary, generate 10 multiple-choice questions.
    Each question should have exactly 4 options: a), b), c), d)

    ✅ Do NOT provide the correct answer below each question.
    ✅ At the end, provide the correct answers in this format:

    Answers:
    1. b)
    2. a)
    3. c)
    ...

    Summary:
    {summary}
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()

# 🎯 Main process function
def process_pdf(file):
    content = extract_pdf_text(file)
    summary = summarize_content(content)
    mcqs = generate_mcqs_from_summary(summary)
    return summary, mcqs

# 🎀 Cute UI using Gradio
with gr.Blocks(theme=gr.themes.Soft(primary_hue="pink", font="poppins")) as demo:
    gr.Markdown("""
        <div style="text-align:center; margin-bottom:20px">
            <h1 style="font-size:2.5em; color:#E91E63;">💗 Study Buddy: PDF to Quiz</h1>
            <p style="color:#555;">Upload your study PDF and get a cute quiz instantly ✨</p>
        </div>
    """)

    with gr.Row(equal_height=True):
        file_input = gr.File(label="📄 Upload Your Study Material (PDF)", file_types=[".pdf"])

    with gr.Row():
        run_button = gr.Button("🌸 Generate Summary & Quiz", size="lg")

    with gr.Row():
        summary_output = gr.Textbox(label="📌 Key Summary", lines=6, interactive=False)
        mcq_output = gr.Textbox(label="📝 Quiz Questions + Answers", lines=18, interactive=False)

    run_button.click(fn=process_pdf, inputs=[file_input], outputs=[summary_output, mcq_output])

demo.launch()

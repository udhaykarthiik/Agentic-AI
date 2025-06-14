import gradio as gr
import requests
import google.generativeai as genai

# 🔐 API Keys (Replace with your actual keys)
GEMINI_API_KEY = "AIzaSyDCPZvnagJobQ4Ne-a3XGKXjPHn5uD42gw"
TAVILY_API_KEY = "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"

# Gemini setup
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Tavily web search function
def search_web(query):
    try:
        response = requests.post(
            "https://api.tavily.com/search",
            json={
                "api_key": TAVILY_API_KEY,
                "query": query,
                "max_results": 5,
                "include_answer": False,
                "include_raw_content": False
            }
        )
        response.raise_for_status()
        return response.json().get("results", [])
    except Exception as e:
        return f"❌ Tavily API Error: {e}"

# Gemini summarization
def analyze_with_gemini(business_type, location, results):
    if isinstance(results, str):
        return results

    context = "\n\n".join([
        f"Title: {r['title']}\nContent: {r['content']}\nURL: {r['url']}"
        for r in results
    ])

    prompt = f"""
You are a business analyst. Based on the following search results about {business_type} businesses in {location}, provide:

1. Top 3 competitors and their strengths.
2. Estimate of daily footfall and peak hours.
3. One strategic recommendation for entering this market.

Search Results:
{context}
"""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Gemini API Error: {e}"

# ✅ Final chatbot function
def chatbot_response(messages, state, business_type):
    # Safely extract the latest message
    if isinstance(messages, list) and isinstance(messages[-1], dict):
        user_message = messages[-1].get("content", "").strip()
    elif isinstance(messages, str):
        user_message = messages.strip()
    else:
        return {"role": "assistant", "content": "❌ Invalid message format."}

    if not user_message:
        return {"role": "assistant", "content": "⚠️ Please enter a location."}

    location = user_message
    query = f"{business_type} businesses in {location}"

    # Search web
    results = search_web(query)
    if isinstance(results, str):
        return {"role": "assistant", "content": results}
    if not results:
        return {"role": "assistant", "content": f"❌ No {business_type} businesses found in {location}."}

    # Analyze with Gemini
    insights = analyze_with_gemini(business_type, location, results)
    return {"role": "assistant", "content": f"📊 Insights for {business_type} in {location}:\n\n{insights}"}

# ✅ Gradio UI
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("## 🧠 Local Business Analyzer")
    gr.Markdown("Get AI-powered insights into any local business category.")

    business_type = gr.Dropdown(
        label="📂 Select Business Type",
        choices=["Clothing Store", "Restaurant", "Gym", "Beauty Salon", "Mobile Store", "Clinic", "Bookstore"],
        value="Clothing Store"
    )

    chat = gr.ChatInterface(
        fn=lambda messages, state, btype: chatbot_response(messages, state, btype),
        chatbot=gr.Chatbot(label="🛍️ Business Bot"),
        textbox=gr.Textbox(placeholder="e.g. T Nagar, Chennai", label="📍 Location"),
        additional_inputs=[business_type],
        type="messages"
    )

if __name__ == "__main__":
    demo.launch()

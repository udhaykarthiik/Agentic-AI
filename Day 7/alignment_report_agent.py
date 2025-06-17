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

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.schema import Document

# ✅ Dummy docs for RAG
docs = [
    "Founders with mismatched values often split when faced with stress.",
    "Draft founder agreements outlining equity and decision paths.",
    "Align risk appetite to navigate startup volatility.",
    "Communication breakdowns are the top cause of splits.",
    "Set role-based boundaries to reduce friction."
]

documents = [Document(page_content=doc) for doc in docs]
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma.from_documents(documents, embeddings, collection_name="founder_docs")
rag_chain = RetrievalQA.from_chain_type(llm=llm, retriever=db.as_retriever(), chain_type="stuff")

def alignment_report(input_text: str) -> str:
    """Generate best practices and founder alignment tips."""
    return rag_chain.run(input_text)

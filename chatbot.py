# Save this as chatbot.py (or your Streamlit page)

import streamlit as st
import wikipediaapi
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import faiss
import numpy as np
import torch

# 1. Fetch Wikipedia data (small excerpts)
@st.cache_data(show_spinner=True)
def fetch_wiki_pages(pages, lang='en'):
    wiki = wikipediaapi.Wikipedia(language=lang, user_agent='chatbot (contact: blog.gourav77@gmail.com)')
    data = []
    for title in pages:
        page = wiki.page(title)
        if page.exists():
            # Take first 1000 chars for memory reasons
            data.append({'title': page.title, 'text': page.text[:1000]})
    return data

# 2. Build FAISS index with MiniLM embeddings
@st.cache_resource(show_spinner=True)
def build_faiss_index(docs):
    model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
    corpus = [doc['text'] for doc in docs]
    embeddings = model.encode(corpus, convert_to_numpy=True)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return model, index, corpus

# 3. Load QA model (small English distilbert for stability)
@st.cache_resource(show_spinner=True)
def load_qa_model():
    model_name = "distilbert-base-cased-distilled-squad"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForQuestionAnswering.from_pretrained(model_name)
    return tokenizer, model

# 4. Retrieve relevant context from FAISS
def retrieve_context(query, embed_model, faiss_index, corpus, top_k=1):
    q_emb = embed_model.encode([query], convert_to_numpy=True)
    D, I = faiss_index.search(q_emb, top_k)
    context = " ".join([corpus[idx] for idx in I[0]])
    return context

# 5. Generate answer using QA model
def generate_answer(question, context, tokenizer, model):
    inputs = tokenizer.encode_plus(question, context, return_tensors='pt', truncation=True, max_length=512)
    input_ids = inputs['input_ids']
    attention_mask = inputs['attention_mask']

    with torch.no_grad():
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)

    start_scores = outputs.start_logits
    end_scores = outputs.end_logits

    answer_start = torch.argmax(start_scores)
    answer_end = torch.argmax(end_scores) + 1

    answer_tokens = input_ids[0][answer_start:answer_end]
    answer = tokenizer.decode(answer_tokens, skip_special_tokens=True)

    if answer.strip() == "":
        answer = "Sorry, I could not find an answer to your question."

    return answer

# -------------------------
# Streamlit UI
st.title("🌐 Mini QA Chatbot")

# Simple Wikipedia pages for test
wiki_pages = ["Artificial intelligence", "Machine learning", "Deep learning"]

with st.spinner("Loading Wikipedia data..."):
    wiki_data = fetch_wiki_pages(wiki_pages)

with st.spinner("Building embeddings and FAISS index..."):
    embed_model, faiss_index, corpus = build_faiss_index(wiki_data)

with st.spinner("Loading QA model..."):
    tokenizer, qa_model = load_qa_model()

user_question = st.text_input("Ask me anything:")

if user_question:
    st.write(f"**You asked:** {user_question}")

    # Get context
    context = retrieve_context(user_question, embed_model, faiss_index, corpus)
    st.write(f"**Context snippet:** {context[:300]}...")

    # Get answer
    answer = generate_answer(user_question, context, tokenizer, qa_model)
    st.success(answer)
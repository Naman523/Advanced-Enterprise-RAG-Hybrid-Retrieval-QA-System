import streamlit as st
import requests

# ------------------ Page Config ------------------
st.set_page_config(
    page_title="AstraRAG – Enterprise PDF Chatbot",
    page_icon="🤖",
    layout="centered"
)

# ------------------ Header ------------------
st.title("📄 AstraRAG")
st.caption("Enterprise-grade PDF Question Answering System")

st.divider()

# ------------------ Query Input ------------------
query = st.text_input(
    "💬 Enter your question",
    placeholder="Ask something from your uploaded documents..."
)

# ------------------ Query Handling ------------------
if query:
    with st.spinner("🔎 Searching your documents..."):
        try:
            response = requests.get(
                "http://127.0.0.1:8000/ask",
                params={"q": query},
                timeout=180
            )

            if response.status_code == 200:
                data = response.json()

                # -------- Answer --------
                st.subheader("✅ Answer")
                st.write(data.get("answer", "No answer returned."))

                # -------- Sources --------
                sources = data.get("sources", [])
                if sources:
                    st.subheader("📚 Sources")
                    for src in sources:
                        source_name = src.get("source", "Unknown")
                        page_no = src.get("page", "N/A")
                        st.write(f"- **{source_name}**, page {page_no}")

            else:
                st.error("❌ API returned an error.")

        except requests.exceptions.RequestException as e:
            st.error(f"❌ Could not connect to backend API: {e}")

# ------------------ Footer ------------------
st.divider()
st.caption("⚡ Powered by Hybrid RAG + Cross-Encoder Re-Ranking")

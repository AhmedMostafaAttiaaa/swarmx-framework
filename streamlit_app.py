"""Very small Swarm-X test UI: streamlit run streamlit_app.py"""
import asyncio
import os
import streamlit as st
from swarm_x.config import load_dotenv
from swarm_x.quickstart import build_baseline_engine
from swarm_x.tools import SerperSearchTool

load_dotenv()
st.set_page_config(page_title="Swarm-X", page_icon="🐝")
st.title("Swarm-X Agent Tester")
st.caption("Run a tiny Gemini or local Ollama agent workflow.")

provider = st.selectbox("Provider", ["gemini", "ollama"], index=0 if os.getenv("PROVIDER", "ollama") == "gemini" else 1)
task = st.text_area("Task", "Give me three Git repository name ideas for this project and recommend one.", height=120)
use_search = st.checkbox("Use Serper web search first", value=False)

if st.button("Run agent", type="primary") and task.strip():
    async def run():
        prompt = task.strip()
        if use_search:
            search = SerperSearchTool()
            findings = await search.search_text(prompt)
            prompt = f"Use these web search results as additional context:\n{findings}\n\nTask:\n{prompt}"
        return await build_baseline_engine(provider).run(prompt)
    try:
        with st.spinner("Running agents..."):
            result = asyncio.run(run())
        st.subheader("Response")
        st.write(result.response)
        with st.expander("Execution details"):
            st.json({"iterations": result.iterations, "events": [event.type for event in result.events]})
    except Exception as exc:
        st.error(str(exc))

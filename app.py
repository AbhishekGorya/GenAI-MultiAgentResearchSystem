"""
Streamlit GUI for the GenAI Multi-Agent Research System.

Wraps the existing agents.py pipeline (Search Agent -> Reader Agent ->
Writer Chain -> Critic Chain) in a simple web interface.

Run with:
    streamlit run app.py
"""

import os
import traceback

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# On Streamlit Community Cloud, secrets are provided via st.secrets (set in
# the app's "Secrets" panel) rather than a .env file. Copy them into
# os.environ here so the rest of the app (and tools.py / agents.py, which
# read os.getenv) picks them up automatically without the user having to
# paste keys into the sidebar every time. Wrapped in try/except because
# st.secrets raises if no secrets.toml exists at all (e.g. running locally
# without one) — that's fine, we just fall through to the sidebar inputs.
for _key in ("MISTRAL_API_KEY", "TAVILY_API_KEY"):
    if not os.getenv(_key):
        try:
            if _key in st.secrets:
                os.environ[_key] = st.secrets[_key]
        except Exception:
            pass

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 AI Research Assistant")
st.caption("Multi-Agent Research Pipeline — LangChain + Mistral AI + Tavily")

# --------------------------------------------------------------------
# Sidebar: API key configuration
# --------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Configuration")

    # IMPORTANT: never pre-fill a text_input's value with a real secret.
    # This app is public — anyone can click the password-field's reveal
    # icon and read whatever value is sitting in the box. If keys are
    # already loaded (from Streamlit Cloud secrets or a local .env), we
    # just show a status message and use them silently. The input boxes
    # only appear — empty — when a key is genuinely missing, so a visitor
    # can never see keys they didn't type in themselves.
    mistral_preloaded = bool(os.getenv("MISTRAL_API_KEY"))
    tavily_preloaded = bool(os.getenv("TAVILY_API_KEY"))

    if not mistral_preloaded:
        entered = st.text_input("Mistral API Key", value="", type="password")
        if entered:
            os.environ["MISTRAL_API_KEY"] = entered
            mistral_preloaded = True

    if not tavily_preloaded:
        entered = st.text_input("Tavily API Key", value="", type="password")
        if entered:
            os.environ["TAVILY_API_KEY"] = entered
            tavily_preloaded = True

    keys_ready = mistral_preloaded and tavily_preloaded

    if keys_ready:
        st.success("API keys loaded ✅")
    else:
        st.warning("Enter both API keys (or set them in Streamlit secrets / your .env file) to run the pipeline.")

    st.caption(
        "Note: if you change a key here after the app has already run once, "
        "restart the app for it to take effect (the search tool is initialized "
        "once when the app first imports its modules)."
    )

    st.divider()
    st.markdown("[Get a Mistral API key](https://console.mistral.ai/)")
    st.markdown("[Get a Tavily API key](https://app.tavily.com/)")

# --------------------------------------------------------------------
# Main input
# --------------------------------------------------------------------
topic = st.text_input(
    "Research topic",
    placeholder="e.g. Artificial Intelligence in Healthcare",
)

start = st.button("🚀 Start Research", disabled=not keys_ready, use_container_width=True)

if "result" not in st.session_state:
    st.session_state.result = None

# --------------------------------------------------------------------
# Pipeline run
# --------------------------------------------------------------------
if start:
    if not topic.strip():
        st.error("Please enter a research topic.")
    else:
        # Imported here (not at module top) so that any API keys entered
        # in the sidebar on this run are already in os.environ before the
        # modules that read them at import time (tools.py, agents.py) load.
        try:
            from agents import (
                build_search_agent,
                build_reader_agent,
                writer_chain,
                critic_chain,
            )
        except Exception as e:
            st.error(
                "Could not import the pipeline modules. Make sure all packages "
                "in requirements.txt are installed.\n\n"
                f"Error: {e}"
            )
            st.stop()

        state = {}

        with st.status("Running research pipeline...", expanded=True) as status:
            try:
                # ------------------------------------------------
                # Step 1 - Search Agent
                # ------------------------------------------------
                st.write("**Step 1/4** — Searching the web...")
                search_agent = build_search_agent()
                search_result = search_agent.invoke(
                    {
                        "messages": [
                            (
                                "user",
                                f"Find recent, reliable and detailed information about: {topic}",
                            )
                        ]
                    }
                )
                state["search_results"] = search_result["messages"][-1].content
                st.write("✅ Search complete")
                with st.expander("🔍 Search results"):
                    st.markdown(state["search_results"])

                # ------------------------------------------------
                # Step 2 - Reader Agent
                # ------------------------------------------------
                st.write("**Step 2/4** — Reading the most relevant page...")
                reader_agent = build_reader_agent()
                reader_result = reader_agent.invoke(
                    {
                        "messages": [
                            (
                                "user",
                                f"Based on the following search results about '{topic}', "
                                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                                f"Search Results:\n{state['search_results'][:800]}",
                            )
                        ]
                    }
                )
                state["scraped_content"] = reader_result["messages"][-1].content
                st.write("✅ Reading complete")
                with st.expander("📄 Scraped content"):
                    st.markdown(state["scraped_content"])

                # ------------------------------------------------
                # Step 3 - Writer Chain
                # ------------------------------------------------
                st.write("**Step 3/4** — Drafting the report...")
                research_combined = (
                    f"Search Results:\n{state['search_results']}\n\n"
                    f"Detailed Scraped Content:\n{state['scraped_content']}\n"
                )
                state["report"] = writer_chain.invoke(
                    {"topic": topic, "research": research_combined}
                )
                st.write("✅ Report drafted")

                # ------------------------------------------------
                # Step 4 - Critic Chain
                # ------------------------------------------------
                st.write("**Step 4/4** — Critiquing the report...")
                state["feedback"] = critic_chain.invoke({"report": state["report"]})
                st.write("✅ Critique complete")

                status.update(label="Pipeline complete ✅", state="complete", expanded=False)
                st.session_state.result = state
                st.session_state.topic = topic

            except Exception as e:
                status.update(label="Pipeline failed ❌", state="error", expanded=True)
                st.error(f"Something went wrong during the pipeline: {e}")
                st.code(traceback.format_exc())
                st.session_state.result = None

# --------------------------------------------------------------------
# Results
# --------------------------------------------------------------------
if st.session_state.result:
    result = st.session_state.result

    st.divider()
    st.subheader("📝 Research Report")
    st.markdown(result["report"])

    st.download_button(
        "⬇️ Download report (.md)",
        data=result["report"],
        file_name=f"{st.session_state.get('topic', 'research')}_report.md".replace(" ", "_"),
        mime="text/markdown",
        use_container_width=True,
    )

    st.subheader("🧐 Critic Feedback")
    st.markdown(result["feedback"])

    col1, col2 = st.columns(2)
    with col1:
        with st.expander("🔍 Raw search results"):
            st.markdown(result["search_results"])
    with col2:
        with st.expander("📄 Raw scraped content"):
            st.markdown(result["scraped_content"])
elif not start:
    st.info("Enter a topic and click **Start Research** to run the pipeline.")

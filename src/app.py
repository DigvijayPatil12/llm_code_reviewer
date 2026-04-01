import streamlit as st
from dotenv import load_dotenv
from github_client import GitHubClient
from llm_orchestrator import LLMOrchestrator

load_dotenv()

st.set_page_config(page_title="AI Code Auditor Pro", page_icon="⚡", layout="wide")

# Initialize Session State to prevent AttributeError
if "report" not in st.session_state: st.session_state.report = None
if "diff" not in st.session_state: st.session_state.diff = None
if "chat_history" not in st.session_state: st.session_state.chat_history = []

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Analysis Settings")
    mode = st.radio("Review Mode:", ["Pull Request", "Full Repo Audit"])
    
    st.markdown("---")
    # Updated model list to avoid 404 NOT_FOUND
    selected_model = st.selectbox(
        "Select AI Model:",
        options=[
            "gemini-2.5-flash",        # Recommended: Best balance of speed/quota
            "gemini-2.5-pro",          # Best for complex architecture
            "gemini-3-flash-preview",  # Newest tech
        ],
        help="Note: Gemini 1.5 models have been deprecated and retired."
    )
    
    strictness = st.slider("AI Strictness", 0.0, 1.0, 0.2)
    
    if st.button("🗑️ Reset Application", use_container_width=True):
        st.session_state.report = None
        st.session_state.diff = None
        st.session_state.chat_history = []
        st.rerun()

# --- MAIN UI ---
st.title("⚡ Universal AI Code Auditor")
repo_input = st.text_input("GitHub Repository URL or 'owner/repo'", placeholder="e.g., DigvijayPatil12/LinkVault")

if mode == "Pull Request":
    pr_input = st.number_input("PR Number", min_value=1, value=1, step=1)
else:
    st.info("💡 **Full Repo Audit**: The AI will scan core files to analyze project architecture.")

if st.button("🚀 Start AI Audit", type="primary"):
    if not repo_input:
        st.warning("Please enter a repository.")
    else:
        # Clean URL to get owner/repo format
        clean_repo = repo_input.replace("https://github.com/", "").replace(".git", "").strip("/")
        
        github = GitHubClient()
        orchestrator = LLMOrchestrator(model_name=selected_model, strictness=strictness)

        with st.spinner(f"📥 Extracting code from {clean_repo}..."):
            try:
                if mode == "Pull Request":
                    content = github.get_pr_diff(clean_repo, pr_input)
                else:
                    content = github.get_full_repo_content(clean_repo)

                if content:
                    with st.spinner(f"🧠 {selected_model} experts are auditing..."):
                        report = orchestrator.generate_review(content)
                        st.session_state.report = report
                        st.session_state.diff = content
                        st.session_state.chat_history = []
                else:
                    st.error("No code found. Check repository/PR details.")
            except Exception as e:
                st.error(f"❌ API Error: {str(e)}")

# --- RESULTS DISPLAY ---
if st.session_state.report:
    st.success("✅ Audit Complete!")
    st.download_button("📥 Download Report", st.session_state.report, "AI_Audit.md")

    tab1, tab2 = st.tabs(["📑 AI Report", "📜 Source Code"])
    with tab1: st.markdown(st.session_state.report)
    with tab2: st.code(st.session_state.diff, language="python")

    st.markdown("---")
    st.subheader("💬 Chat with the Reviewer")
    
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if user_q := st.chat_input("Ask a question about this code..."):
        st.session_state.chat_history.append({"role": "user", "content": user_q})
        
        # Immediate processing for chat
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                orchestrator = LLMOrchestrator(model_name=selected_model, strictness=strictness)
                answer = orchestrator.answer_followup(
                    st.session_state.diff, 
                    st.session_state.report, 
                    user_q
                )
                st.markdown(answer)
                st.session_state.chat_history.append({"role": "assistant", "content": answer})
        st.rerun()
"""
IT Helpdesk Agent — Streamlit Live Chat UI
Role D deliverable: reuses run_model_tool_loop from chat.py.

Run with:
    streamlit run app.py
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st

# ── Ensure starter_v0 is importable ──────────────────────────────────
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from env_loader import load_lab_env
from providers import make_provider
from tools import TOOL_FUNCTIONS, load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version

# Reuse the SAME loop that CLI and eval use — lab requirement §9 / §13
from chat import run_model_tool_loop, write_transcript, now_iso, safe_slug, trim_history

load_lab_env(ROOT)

# ── Constants ────────────────────────────────────────────────────────
ARTIFACTS_DIR = ROOT / "artifacts"
TRANSCRIPTS_DIR = ROOT / "transcripts"
PROVIDERS = ["gemini", "openrouter", "openai", "anthropic"]
VERSIONS = ["v0", "v1", "v2", "v3"]

# Tool name → emoji mapping for visual clarity
TOOL_ICONS = {
    "clarify": "❓",
    "search_kb": "📚",
    "check_service_status": "🌐",
    "inspect_device": "💻",
    "lookup_user": "👤",
    "format_incident_report": "📝",
    "policy": "📜",
    "create_ticket": "🎫",
    "search_device_info": "🔍",
}

# ── Page config ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="IT Helpdesk Agent — Northstar Labs",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* Global */
.stApp {
    font-family: 'Inter', sans-serif;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0c1222 0%, #131b30 100%);
    border-right: 1px solid rgba(99, 102, 241, 0.15);
}
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown span,
section[data-testid="stSidebar"] label {
    color: #cbd5e1;
}

/* Header */
.app-header {
    text-align: center;
    padding: 0.5rem 0 0.2rem 0;
}
.app-header h1 {
    background: linear-gradient(135deg, #6366f1 0%, #a78bfa 50%, #818cf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 1.8rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    margin: 0;
    line-height: 1.2;
}
.app-header p {
    color: #64748b;
    font-size: 0.85rem;
    margin: 0.15rem 0 0 0;
}

/* Sidebar header */
.sidebar-title {
    background: linear-gradient(90deg, #818cf8, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 1.35rem;
    font-weight: 800;
    letter-spacing: -0.02em;
}

/* Artifact badge */
.artifact-badge {
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: #fff;
    padding: 5px 14px;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
    display: inline-block;
    margin: 4px 0;
    letter-spacing: 0.01em;
    box-shadow: 0 2px 8px rgba(79, 70, 229, 0.25);
}

/* Hash text */
.hash-text {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: #64748b;
    word-break: break-all;
    line-height: 1.5;
}

/* Info cards in sidebar */
.info-card {
    background: rgba(99, 102, 241, 0.06);
    border: 1px solid rgba(99, 102, 241, 0.12);
    border-radius: 10px;
    padding: 12px 14px;
    margin: 6px 0;
}

/* Tool call display */
.tool-call-card {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.06) 0%, rgba(129, 140, 248, 0.04) 100%);
    border: 1px solid rgba(99, 102, 241, 0.18);
    border-left: 3px solid #6366f1;
    border-radius: 8px;
    padding: 10px 14px;
    margin: 5px 0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82em;
}
.tool-call-card .tool-name {
    color: #818cf8;
    font-weight: 600;
    font-size: 0.95em;
}
.tool-call-card pre {
    margin: 6px 0 0 0;
    white-space: pre-wrap;
    word-break: break-word;
    color: #c4b5fd;
    font-size: 0.9em;
}

/* Tool result display */
.tool-result-card {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.06) 0%, rgba(52, 211, 153, 0.03) 100%);
    border: 1px solid rgba(16, 185, 129, 0.18);
    border-left: 3px solid #10b981;
    border-radius: 8px;
    padding: 10px 14px;
    margin: 5px 0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82em;
}
.tool-result-card pre {
    margin: 6px 0 0 0;
    white-space: pre-wrap;
    word-break: break-word;
    color: #6ee7b7;
    font-size: 0.9em;
    max-height: 300px;
    overflow-y: auto;
}

/* Tool error display */
.tool-error-card {
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.06) 0%, rgba(248, 113, 113, 0.03) 100%);
    border: 1px solid rgba(239, 68, 68, 0.18);
    border-left: 3px solid #ef4444;
    border-radius: 8px;
    padding: 10px 14px;
    margin: 5px 0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82em;
}
.tool-error-card pre {
    margin: 6px 0 0 0;
    white-space: pre-wrap;
    word-break: break-word;
    color: #fca5a5;
    font-size: 0.9em;
}

/* Round header */
.round-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 8px 0 4px 0;
    font-size: 0.8rem;
    color: #94a3b8;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.round-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #6366f1;
    display: inline-block;
}

/* Status pills */
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 3px 12px;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.02em;
    margin-top: 6px;
}
.status-answered {
    background: rgba(16, 185, 129, 0.12);
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.25);
}
.status-waiting {
    background: rgba(245, 158, 11, 0.12);
    color: #fbbf24;
    border: 1px solid rgba(245, 158, 11, 0.25);
}
.status-error {
    background: rgba(239, 68, 68, 0.12);
    color: #f87171;
    border: 1px solid rgba(239, 68, 68, 0.25);
}

/* Metric row in sidebar */
.metric-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 3px 0;
    font-size: 0.82rem;
}
.metric-label { color: #94a3b8; }
.metric-value { color: #e2e8f0; font-weight: 600; font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; }

/* Tool count summary */
.tool-summary {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    background: rgba(99, 102, 241, 0.08);
    border: 1px solid rgba(99, 102, 241, 0.15);
    padding: 2px 10px;
    border-radius: 999px;
    font-size: 0.72rem;
    color: #a5b4fc;
    font-weight: 500;
    margin: 2px 2px;
}
</style>
""", unsafe_allow_html=True)


# ── Session state initialization ─────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "history" not in st.session_state:
    st.session_state.history = []
if "turn_index" not in st.session_state:
    st.session_state.turn_index = 0
if "transcript" not in st.session_state:
    st.session_state.transcript = None
if "transcript_path" not in st.session_state:
    st.session_state.transcript_path = None
if "total_tool_calls" not in st.session_state:
    st.session_state.total_tool_calls = 0
if "tool_call_counts" not in st.session_state:
    st.session_state.tool_call_counts = {}


# ── Sidebar ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="sidebar-title">🛠️ Northstar IT Agent</p>', unsafe_allow_html=True)
    st.caption("Internal Helpdesk — Day 04 Lab")
    st.divider()

    # ─ Provider & model config ─
    st.markdown("**⚙️ Configuration**")
    provider_name = st.selectbox("Provider", PROVIDERS, index=0, label_visibility="collapsed",
                                  help="Model provider to use")
    col_v, col_m = st.columns([1, 1])
    with col_v:
        version_label = st.selectbox("Version", VERSIONS, index=len(VERSIONS) - 1)
    with col_m:
        model_override = st.text_input("Model", value="", placeholder="default",
                                        help="Leave blank for provider default model")

    with st.expander("Advanced", expanded=False):
        history_window = st.slider("Context window (turns)", 1, 10, 5)
        max_tool_rounds = st.slider("Max tool rounds", 1, 8, 4)

    st.divider()

    # ─ Artifact version & hashes ─
    system_prompt_path = ARTIFACTS_DIR / "system_prompt.md"
    tools_path = ARTIFACTS_DIR / "tools.yaml"

    try:
        artifact_version = build_artifact_version(version_label, system_prompt_path, tools_path)
        av = artifact_version_dict(artifact_version)

        st.markdown("**📋 Artifact Version**")
        st.markdown(f'<span class="artifact-badge">{av["artifact_version"]}</span>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="info-card">'
            f'<div class="metric-row"><span class="metric-label">Prompt</span>'
            f'<span class="metric-value">{av["prompt_hash"][:16]}…</span></div>'
            f'<div class="metric-row"><span class="metric-label">Tools</span>'
            f'<span class="metric-value">{av["tools_hash"][:16]}…</span></div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    except Exception as e:
        st.error(f"Artifact error: {e}")
        artifact_version = None

    st.divider()

    # ─ Session stats ─
    st.markdown("**📊 Session Stats**")
    n_turns = st.session_state.turn_index
    n_tools = st.session_state.total_tool_calls
    st.markdown(
        f'<div class="info-card">'
        f'<div class="metric-row"><span class="metric-label">Turns</span>'
        f'<span class="metric-value">{n_turns}</span></div>'
        f'<div class="metric-row"><span class="metric-label">Tool calls</span>'
        f'<span class="metric-value">{n_tools}</span></div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Tool usage breakdown
    if st.session_state.tool_call_counts:
        tool_summary_html = ""
        for tname, tcount in sorted(st.session_state.tool_call_counts.items(), key=lambda x: -x[1]):
            icon = TOOL_ICONS.get(tname, "🔧")
            tool_summary_html += f'<span class="tool-summary">{icon} {tname} ×{tcount}</span> '
        st.markdown(tool_summary_html, unsafe_allow_html=True)

    st.divider()

    # ─ Transcript ─
    if st.session_state.transcript_path:
        st.markdown("**📝 Transcript**")
        rel_path = st.session_state.transcript_path
        st.code(str(rel_path), language=None)

    # ─ Available tools ─
    with st.expander("🧰 Available Tools", expanded=False):
        for tname in TOOL_FUNCTIONS:
            icon = TOOL_ICONS.get(tname, "🔧")
            st.markdown(f"{icon} `{tname}`")

    st.divider()

    # ─ Actions ─
    if st.button("🗑️ Clear Chat", use_container_width=True, type="secondary"):
        st.session_state.messages = []
        st.session_state.history = []
        st.session_state.turn_index = 0
        st.session_state.transcript = None
        st.session_state.transcript_path = None
        st.session_state.total_tool_calls = 0
        st.session_state.tool_call_counts = {}
        st.rerun()


# ── Helper: render tool trace ────────────────────────────────────────
def render_tool_trace(rounds: list[dict[str, Any]]) -> None:
    """Display each round's tool calls and results with styled cards."""
    for rnd in rounds:
        round_num = rnd.get("round", "?")
        tool_calls = rnd.get("tool_calls", [])
        tool_results = rnd.get("tool_results", [])

        if not tool_calls:
            continue

        # Build summary of tools in this round
        tool_names = [tc.get("name", "?") for tc in tool_calls]
        icons = " ".join(TOOL_ICONS.get(n, "🔧") for n in tool_names)
        names = ", ".join(tool_names)

        with st.expander(f"{icons}  Round {round_num} — {names}", expanded=True):
            for i, tc in enumerate(tool_calls):
                name = tc.get("name", "unknown")
                args = tc.get("args", {})
                icon = TOOL_ICONS.get(name, "🔧")
                args_json = json.dumps(args, ensure_ascii=False, indent=2, default=str)

                # Tool call card
                st.markdown(
                    f'<div class="tool-call-card">'
                    f'<span class="tool-name">{icon} {name}</span>'
                    f'<pre>{args_json}</pre>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

                # Matching result
                if i < len(tool_results):
                    tr = tool_results[i]
                    result = tr.get("result", {})
                    is_error = isinstance(result, dict) and result.get("error")
                    result_json = json.dumps(result, ensure_ascii=False, indent=2, default=str)

                    if is_error:
                        st.markdown(
                            f'<div class="tool-error-card">'
                            f'<strong>❌ Error</strong>'
                            f'<pre>{result_json}</pre>'
                            f'</div>',
                            unsafe_allow_html=True,
                        )
                    else:
                        display = result_json if len(result_json) < 2000 else result_json[:2000] + "\n…(truncated)"
                        st.markdown(
                            f'<div class="tool-result-card">'
                            f'<strong>✅ Result</strong>'
                            f'<pre>{display}</pre>'
                            f'</div>',
                            unsafe_allow_html=True,
                        )


def render_status(status: str) -> None:
    """Show a styled status pill."""
    pills = {
        "answered": ("✓ Answered", "status-answered"),
        "waiting_for_user": ("⏳ Waiting for user", "status-waiting"),
        "max_tool_rounds": ("⚠ Max rounds", "status-error"),
        "provider_error": ("✗ Error", "status-error"),
    }
    label, css = pills.get(status, (status, "status-error"))
    st.markdown(f'<span class="status-pill {css}">{label}</span>', unsafe_allow_html=True)


# ── Main chat area ───────────────────────────────────────────────────
st.markdown(
    '<div class="app-header">'
    '<h1>💬 IT Helpdesk Chat</h1>'
    f'<p>Provider: {provider_name} · Version: {version_label}'
    f'{" · Model: " + model_override if model_override else ""}</p>'
    '</div>',
    unsafe_allow_html=True,
)

# Welcome message when empty
if not st.session_state.messages:
    st.markdown("---")
    cols = st.columns(3)
    examples = [
        ("🌐 Service Status", "VPN có đang gặp sự cố không?"),
        ("💻 Device Check", "Kiểm tra tình trạng thiết bị LT-318"),
        ("📚 Knowledge Base", "Hướng dẫn kết nối VPN trên macOS"),
    ]
    for col, (title, query) in zip(cols, examples):
        with col:
            st.markdown(f"**{title}**")
            st.caption(query)
    st.markdown("---")

# Render existing messages
for msg in st.session_state.messages:
    role = msg["role"]
    with st.chat_message(role, avatar="🧑‍💻" if role == "user" else "🤖"):
        if role == "user":
            st.markdown(msg["content"])
        else:
            # Tool trace first, then response
            if "tool_trace" in msg:
                render_tool_trace(msg["tool_trace"])
            st.markdown(msg["content"])
            if "status" in msg:
                render_status(msg["status"])

# ── Chat input ───────────────────────────────────────────────────────
user_input = st.chat_input("Nhập câu hỏi IT helpdesk…")

if user_input:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(user_input)

    # Prepare model call
    try:
        system_prompt = system_prompt_path.read_text(encoding="utf-8")
        tool_declarations = load_tool_declarations(tools_path)
        openai_tools = to_openai_tools(tool_declarations)
        provider = make_provider(provider_name)
        selected_model = model_override if model_override else getattr(provider, "default_model", None)
    except Exception as e:
        with st.chat_message("assistant", avatar="🤖"):
            st.error(f"⚠️ Setup error: {e}")
        st.stop()

    # Initialize transcript on first turn
    st.session_state.turn_index += 1
    if st.session_state.transcript is None:
        timestamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")
        transcript_id = "_".join([
            safe_slug(version_label),
            safe_slug(provider_name),
            "ui",
            timestamp,
        ])
        transcript_path = TRANSCRIPTS_DIR / f"{transcript_id}.transcript.json"
        st.session_state.transcript_path = transcript_path
        st.session_state.transcript = {
            "transcript_id": transcript_id,
            **(artifact_version_dict(artifact_version) if artifact_version else {}),
            "provider": provider_name,
            "model": selected_model,
            "system_prompt": str(system_prompt_path),
            "tools": str(tools_path),
            "history_window": history_window,
            "max_tool_rounds": max_tool_rounds,
            "created_at": now_iso(),
            "updated_at": now_iso(),
            "turns": [],
        }

    # Build messages for model
    messages = [
        {"role": "system", "content": system_prompt},
        *trim_history(st.session_state.history, history_window),
        {"role": "user", "content": user_input},
    ]

    # Run the agent loop (REUSING run_model_tool_loop from chat.py)
    turn_record: dict[str, Any] = {
        "turn_index": st.session_state.turn_index,
        "started_at": now_iso(),
        "user": user_input,
        "status": "started",
        "assistant_text": None,
        "rounds": [],
        "tool_events": [],
    }

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("🤔 Agent đang xử lý…"):
            try:
                result = run_model_tool_loop(
                    provider=provider,
                    messages=messages,
                    tools=openai_tools,
                    model=selected_model,
                    max_tool_rounds=max_tool_rounds,
                )
                turn_record.update(result)

                assistant_text = result.get("assistant_text", "")
                status = result.get("status", "unknown")
                rounds = result.get("rounds", [])

                # Show tool trace
                if rounds:
                    render_tool_trace(rounds)

                    # Update tool stats
                    for rnd in rounds:
                        for tc in rnd.get("tool_calls", []):
                            tname = tc.get("name", "unknown")
                            st.session_state.total_tool_calls += 1
                            st.session_state.tool_call_counts[tname] = (
                                st.session_state.tool_call_counts.get(tname, 0) + 1
                            )

                # Show final response
                st.markdown(assistant_text)
                render_status(status)

                # Update history
                st.session_state.history.append({"role": "user", "content": user_input})
                st.session_state.history.append({"role": "assistant", "content": assistant_text})

                # Store for re-rendering
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": assistant_text,
                    "tool_trace": rounds,
                    "status": status,
                })

            except Exception as exc:
                error_msg = f"{type(exc).__name__}: {str(exc)}"
                turn_record.update({
                    "status": "provider_error",
                    "error": error_msg,
                })
                st.error(f"⚠️ Provider error: {error_msg}")
                render_status("provider_error")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"⚠️ Error: {error_msg}",
                    "status": "provider_error",
                })

    # Save transcript
    turn_record["ended_at"] = now_iso()
    st.session_state.transcript["turns"].append(turn_record)
    write_transcript(st.session_state.transcript_path, st.session_state.transcript)

import streamlit as st
import os
import sys
import time
import shutil

# Ensure system paths are configured correctly for rag imports
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from rag.document_processor import process_pdf
from rag.indexer import index_document
from rag.generate_answer import answer_question
from rag.summarizer import summarize_document
from rag.key_points import generate_key_points
from rag.statistics import get_document_statistics
from rag.export_chat import export_chat
from rag.vector_store import clear_vector_database
from rag.export_pdf import export_chat_pdf
from rag.chat_memory import get_chat_context
from rag.logger import save_chat
from rag.chat_manager import (
    create_chat,
    get_chat,
    update_chat_messages,
    rename_chat,
    delete_chat,
    get_all_chats,
    add_file_to_chat,
    get_chat_files,
    auto_title
)
from rag.settings import save_last_chat, load_last_chat

# Import authentication functions from our auth backend module
from rag.auth import register_user, verify_user

# ====================================
# Authentication Layer Gate State Check
# ====================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None

# Dynamic Sidebar & Layout Management based on auth state
if not st.session_state.authenticated:
    st.set_page_config(
        page_title="Sign In - Linguabridge",
        page_icon="🤖",
        layout="centered",  # Centered layout makes the login form clean, spacious, and prominent
        initial_sidebar_state="collapsed"  # Completely hides the sidebar during authentication
    )
else:
    st.set_page_config(
        page_title="Linguabridge - Multilingual PDF Chatbot",
        page_icon="🤖",
        layout="wide",  # Expands to full screen once logged in
        initial_sidebar_state="expanded"
    )

# Standard High-End Premium UI Stylesheet
st.markdown("""
    <style>
        /* Global Reset & Base Typography */
        .stApp {
            background-color: #ffffff;
            color: #0d0d0d;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }
        
        /* 
           1. KEEP THE LOGIN BOX INDENTICAL
           Targets the native block wrapper ONLY when it's wrapping our auth card hook
        */
        div[data-testid="stBlock"]:has(.auth-card) {
            border-radius: 12px !important;
            background-color: #ffffff !important;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05) !important;
            padding: 10px !important;
        }
        
        /* Force form buttons and fields to adapt perfectly to container size */
        div[data-testid="stForm"] {
            border: none !important;
            padding: 0 !important;
        }
        
        /* 
           2. SIDEBAR REALIGNMENT FIX
           Cleans up alignment and padding anomalies from image_f67c6e.png
        */
        section[data-testid="stSidebar"] {
            background-color: #f8f9fa !important;
            border-right: 1px solid #e9ecef;
        }
        
        /* Remove nested block borders inside the sidebar entirely */
        section[data-testid="stSidebar"] div[data-testid="stBlock"] {
            border: none !important;
            box-shadow: none !important;
            background: transparent !important;
            padding: 0 !important;
        }
        
        section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {
            gap: 0.8rem !important;
            padding-left: 0.25rem !important;
            padding-right: 0.25rem !important;
        }
        
        /* Premium Inline Active Row Sub-Menus */
        .menu-popover-tray {
            background-color: #ffffff;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 10px;
            margin-top: 4px;
            margin-bottom: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }
        
        /* Clean Document Badges Container */
        .doc-badge-container {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            padding: 10px 14px;
            background-color: #f1f3f5;
            border-radius: 8px;
            margin-bottom: 20px;
            align-items: center;
        }
        .doc-badge-title {
            font-size: 0.8rem;
            font-weight: 600;
            color: #495057;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .doc-pill {
            background-color: #ffffff;
            color: #212529;
            padding: 2px 10px;
            border-radius: 6px;
            font-size: 0.8rem;
            font-weight: 500;
            border: 1px solid #ced4da;
        }
        
        /* Header Overrides */
        h1, h2, h3 {
            color: #1a1a1a !important;
            font-weight: 600;
        }
    </style>
""", unsafe_allow_html=True)

# Pure Modern Standard Full-Page Auth UI
if not st.session_state.authenticated:
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    
    # 1. Use a native Streamlit container with a border enabled
    with st.container(border=True):
        
        st.markdown("<h1 style='text-align: center; font-size: 2rem; letter-spacing: -0.5px; margin-bottom: 8px;'>Sign in to Linguabridge</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #6c757d; font-size: 0.95rem; margin-bottom: 32px;'>Enter your details below to access your secure workspace.</p>", unsafe_allow_html=True)
        
        auth_mode = st.tabs(["Sign In", "Create Account"])
        
        # ─── SIGN IN VIEW ──────────────────────────────────────
        with auth_mode[0]:
            st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
            with st.form("login_form", clear_on_submit=False):
                username_input = st.text_input("Username", placeholder="your_username").strip()
                password_input = st.text_input("Password", type="password", placeholder="••••••••")
                st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
                
                if st.form_submit_button("Sign In", use_container_width=True, type="primary"):
                    if verify_user(username_input, password_input):
                        st.session_state.authenticated = True
                        st.session_state.username = username_input
                        st.toast("Welcome back! ✨")
                        st.rerun()
                    else:
                        st.error("Invalid credentials. Please verify your username and password.")
                        
        # ─── REGISTER VIEW ────────────────────────────────────
        with auth_mode[1]:
            st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
            with st.form("register_form", clear_on_submit=False):
                reg_username = st.text_input("Choose Username", placeholder="new_user_id").strip()
                reg_password = st.text_input("Create Secure Password", type="password", placeholder="••••••••")
                st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
                
                if st.form_submit_button("Register Account", use_container_width=True):
                    success, msg = register_user(reg_username, reg_password)
                    if success:
                        st.success("Account successfully provisioned! Switch over to 'Sign In'.")
                    else:
                        st.error(msg)
                        
    st.stop()

# ====================================
# Post-Authentication Workspace Code
# ====================================
current_user = st.session_state.username

if "active_menu_chat_id" not in st.session_state:
    st.session_state.active_menu_chat_id = None

if "current_chat" not in st.session_state or st.session_state.current_chat is None:
    last_chat_id = load_last_chat()
    chat_data = get_chat(last_chat_id) if last_chat_id else None
    
    if chat_data and chat_data.get("username", "").strip().lower() == current_user.lower():
        st.session_state.current_chat = last_chat_id
    else:
        new_id = create_chat(current_user)
        st.session_state.current_chat = new_id
        save_last_chat(new_id)

active_chat_id = st.session_state.current_chat
chat_data = get_chat(active_chat_id)

if not chat_data or chat_data.get("username", "").strip().lower() != current_user.lower():
    active_chat_id = create_chat(current_user)
    st.session_state.current_chat = active_chat_id
    save_last_chat(active_chat_id)
    chat_data = get_chat(active_chat_id)

st.session_state.messages = chat_data.get("messages", [])

if "processed_files" not in st.session_state:
    st.session_state.processed_files = get_chat_files(active_chat_id)

UPLOAD_FOLDER = os.path.join("workspace_data", current_user, active_chat_id, "uploads")
TEXT_FOLDER = os.path.join("workspace_data", current_user, active_chat_id, "text_cache")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TEXT_FOLDER, exist_ok=True)

# ====================================
# Sidebar Architecture
# ====================================
with st.sidebar:
    st.markdown("<div style='font-size:1.2rem; font-weight:700; padding:12px 0 6px 0;'>🤖 Linguabridge</div>", unsafe_allow_html=True)
    
    if st.button("➕ New Chat", use_container_width=True):
        new_id = create_chat(current_user)
        st.session_state.current_chat = new_id
        save_last_chat(new_id)
        st.session_state.processed_files = []
        st.session_state.active_menu_chat_id = None
        st.rerun()
        
    st.write("---")

    st.markdown("<div style='font-size:0.8rem; font-weight:600; color:#6c757d; padding-bottom:6px; letter-spacing:0.3px;'>CONVERSATIONS</div>", unsafe_allow_html=True)
    user_chats = get_all_chats(current_user)
    sorted_chats = sorted(
        user_chats.items(),
        key=lambda x: x[1].get("updated_at", x[1].get("created_at", "")),
        reverse=True
    )
    
    if not sorted_chats:
        st.caption("No dynamic history logs recorded.")
    else:
        for cid, cinfo in sorted_chats:
            title = cinfo.get("title", "Untitled Chat")
            is_active = (cid == active_chat_id)
            
            row_col_left, row_col_right = st.columns([0.84, 0.16])
            
            with row_col_left:
                lbl = f"💬 {title}" if is_active else f"   {title}"
                if st.button(lbl, key=f"select_{cid}", use_container_width=True):
                    st.session_state.current_chat = cid
                    save_last_chat(cid)
                    st.session_state.processed_files = get_chat_files(cid)
                    st.session_state.active_menu_chat_id = None
                    st.rerun()
                    
            with row_col_right:
                if st.button("⋮", key=f"h_menu_{cid}", use_container_width=True):
                    if st.session_state.active_menu_chat_id == cid:
                        st.session_state.active_menu_chat_id = None
                    else:
                        st.session_state.active_menu_chat_id = cid
                    st.rerun()
            
            if st.session_state.active_menu_chat_id == cid:
                st.markdown(f'<div class="menu-popover-tray">', unsafe_allow_html=True)
                
                with st.popover("📝 Rename", use_container_width=True):
                    new_label = st.text_input("New Title Text:", value=title, key=f"rename_in_{cid}")
                    if st.button("Apply", key=f"apply_ren_{cid}", use_container_width=True):
                        if new_label.strip():
                            rename_chat(cid, new_label.strip())
                            st.session_state.active_menu_chat_id = None
                            st.toast("Renamed successfully!")
                            st.rerun()
                            
                with st.popover("📥 Export Options", use_container_width=True):
                    target_messages = cinfo.get("messages", [])
                    if not target_messages:
                        st.caption("No chat records to export yet.")
                    else:
                        chat_text = export_chat(target_messages)
                        st.download_button(
                            label="Export as Plaintext (.txt)",
                            data=chat_text,
                            file_name=f"chat_export_{cid}.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                        if st.button("Compile Transcript PDF", key=f"pdf_compile_{cid}", use_container_width=True):
                            pdf_path = export_chat_pdf(target_messages)
                            if os.path.exists(pdf_path):
                                with open(pdf_path, "rb") as pf:
                                    st.download_button(
                                        label="📥 Download Compiled PDF",
                                        data=pf,
                                        file_name=f"chat_export_{cid}.pdf",
                                        mime="application/pdf",
                                        use_container_width=True
                                    )
                                    
                if st.button("🗑 Delete Chat", key=f"delete_act_{cid}", type="secondary", use_container_width=True):
                    delete_chat(cid, current_user)
                    if cid == active_chat_id:
                        remaining = get_all_chats(current_user)
                        next_id = list(remaining.keys())[0] if remaining else create_chat(current_user)
                        st.session_state.current_chat = next_id
                        save_last_chat(next_id)
                        st.session_state.processed_files = get_chat_files(next_id)
                    st.session_state.active_menu_chat_id = None
                    st.toast("Chat data deleted.")
                    st.rerun()
                    
                st.markdown('</div>', unsafe_allow_html=True)

    st.write("---")
    
    st.markdown("<div style='font-size:0.8rem; font-weight:600; color:#6c757d; padding-bottom:5px; letter-spacing:0.3px;'>KNOWLEDGE INGESTION</div>", unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "Drop reference documents here",
        type=["pdf"],
        accept_multiple_files=True,
        key=f"uploader_{st.session_state.current_chat}",
        label_visibility="collapsed"
    )

    st.write("---")
    st.markdown(f"""
        <div style="background-color:#f1f3f5; border-radius:8px; padding:10px; margin-bottom:8px; border:1px solid #dee2e6;">
            <div style="font-size:0.7rem; text-transform:uppercase; color:#6c757d; font-weight:700;">Account Profile</div>
            <div style="font-size:0.9rem; font-weight:600; color:#212529; margin-top:2px; overflow:hidden; text-overflow:ellipsis;">👤 {current_user}</div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚪 Sign Out Workspace", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.current_chat = None
        st.session_state.active_menu_chat_id = None
        if "processed_files" in st.session_state:
            del st.session_state.processed_files
        if "messages" in st.session_state:
            del st.session_state.messages
        st.rerun()

# ====================================
# Main Application Content Flow
# ====================================
if uploaded_files:
    active_chat_files = get_chat_files(active_chat_id)
    new_file_ingested = False
    
    for file in uploaded_files:
        if file.name in active_chat_files:
            continue
            
        file_path = os.path.join(UPLOAD_FOLDER, file.name)
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())
            
        add_file_to_chat(active_chat_id, file.name)
        
        with st.spinner(f"Indexing context vectors: {file.name}..."):
            try:
                document_info = process_pdf(file_path, active_chat_id)
                if document_info and document_info.get("text", "").strip():
                    chunks_created = index_document(
                        document_info["pages_text"],
                        file.name,
                        active_chat_id
                    )
                    st.session_state.processed_files.append(file.name)
                    new_file_ingested = True
                else:
                    st.error(f"Unreadable file contents: {file.name}")
            except Exception as e:
                st.error(f"Error parsing mapping metrics for {file.name}: {str(e)}")
                
    if new_file_ingested:
        st.toast("✅ Active document memory synchronization complete!", icon="🚀")
        time.sleep(0.5)
        st.rerun()

st.markdown(f"<h2 style='margin-bottom: 8px; padding-top:4px;'>{chat_data.get('title', 'New Chat')}</h2>", unsafe_allow_html=True)

active_chat_files = get_chat_files(active_chat_id)
if active_chat_files:
    badge_html = '<div class="doc-badge-container"><span class="doc-badge-title">Attached Context: &nbsp;</span>'
    for f in active_chat_files:
        badge_html += f'<span class="doc-pill">📄 {f}</span>&nbsp;'
    badge_html += '</div>'
    st.markdown(badge_html, unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown("""
        <div style="padding: 24px; background-color: #f8f9fa; border-radius: 8px; border: 1px solid #e9ecef; margin: 10px 0 24px 0;">
            <h3 style="margin-top: 0; font-size: 1.3rem; color:#212529;">👋 Welcome to Linguabridge!</h3>
            <p style="color:#495057; font-size:0.95rem; margin-bottom: 15px;">Your multi-lingual PDF assistant. Let's get started with three simple steps:</p>
            <ol style="color:#495057; font-size:0.95rem; padding-left: 20px; line-height: 1.6;">
                <li><strong>Upload:</strong> Drop one or more PDFs into the file uploader on the left sidebar.</li>
                <li><strong>Ask:</strong> Type any question about your document in the chat bar below.</li>
                <li><strong>Language Support:</strong> Feel free to type and receive answers in English, Tamil, Hindi, Malayalam, Telugu, or your preferred language!</li>
            </ol>
        </div>
    """, unsafe_allow_html=True)

for msg in st.session_state.messages:
    role = msg["role"]
    avatar = "👤" if role == "user" else "🤖"
    if role == "assistant":
        clean_render_content = msg["content"].split("\n\n### Sources\n")[0]
        with st.chat_message(role, avatar=avatar):
            st.markdown(clean_render_content)
    else:
        with st.chat_message(role, avatar=avatar):
            st.markdown(msg["content"])

query_input = st.chat_input("Ask anything in English, Tamil, Hindi, Malayalam, Telugu...")

if query_input:
    st.session_state.messages.append({"role": "user", "content": query_input})
    with st.chat_message("user", avatar="👤"):
        st.markdown(query_input)
        
    if chat_data.get("title") == "New Chat":
        calculated_title = auto_title(query_input)
        rename_chat(active_chat_id, calculated_title)
        
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Synthesizing context sources..."):
            start_timestamp = time.time()
            context_history_block = get_chat_context(st.session_state.messages[:-1])
            
            answer_text, source_references, confidence_score = answer_question(
                query_input,
                active_chat_id,
                context_history_block
            )
            
            save_chat(query_input, answer_text)
            elapsed_time = round(time.time() - start_timestamp, 2)
            st.markdown(answer_text)
            
            meta_col1, meta_col2 = st.columns(2)
            meta_col1.caption(f"⏱ Response Synthesis Duration: {elapsed_time}s")
            meta_col2.caption(f"🎯 Inference Confidence Score: {confidence_score}%")
            
            if source_references:
                with st.expander("📄 Verifiable References & Source Mappings", expanded=False):
                    for src in source_references:
                        st.markdown(f"- {src}")
                        
    complete_response_payload = answer_text
    if source_references:
        complete_response_payload += "\n\n### Sources\n" + "\n".join([f"📄 {s}" for s in source_references])
        
    st.session_state.messages.append({"role": "assistant", "content": complete_response_payload})
    update_chat_messages(active_chat_id, st.session_state.messages)
    st.rerun()
# components/sidebar.py

import streamlit as st
from config.settings import SESSION_KEYS, PAGES
from utils.state_manager import logout_user

def render_sidebar():
    """Render sidebar navigation"""
    st.sidebar.markdown('<h2 style="color: #667eea; font-weight: 600;">🧭 Navigasi</h2>', unsafe_allow_html=True)
    
    if st.sidebar.button("📝 Form Input"):
        st.session_state[SESSION_KEYS["CURRENT_PAGE"]] = PAGES["FORM_INPUT"]
    
    if st.sidebar.button("📊 Dashboard"):
        st.session_state[SESSION_KEYS["CURRENT_PAGE"]] = PAGES["DASHBOARD"]
    
    if st.sidebar.button("🚪 Logout"):
        logout_user()
        st.rerun()

def get_current_page():
    """Get current active page"""
    return st.session_state.get(SESSION_KEYS["CURRENT_PAGE"], PAGES["FORM_INPUT"])
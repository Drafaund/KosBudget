# components/auth.py

import streamlit as st
from utils.state_manager import authenticate_user, register_user

def render_auth_page():
    """Render authentication page"""
    st.markdown('<h1 class="title-gradient">🏠 KosBudget</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 1.2rem; color: white; text-align: center; margin-bottom: 2rem;">Manajemen Keuangan Cerdas untuk Anak Kos</p>', unsafe_allow_html=True)
    
    auth_tab = st.sidebar.radio("🔐 Pilih Aksi", ["Sign In", "Sign Up"])

    if auth_tab == "Sign In":
        render_signin_form()
    elif auth_tab == "Sign Up":
        render_signup_form()

def render_signin_form():
    """Render sign in form"""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="category-card">', unsafe_allow_html=True)
        st.markdown('<h2 class="subtitle-gradient">🔐 Masuk Akun</h2>', unsafe_allow_html=True)
        
        username = st.text_input("👤 Username")
        password = st.text_input("🔒 Password", type="password")
        
        if st.button("🚀 Masuk", key="signin_btn"):
            success, message = authenticate_user(username, password)
            if success:
                st.markdown(f'<div class="success-message">✅ {message}</div>', unsafe_allow_html=True)
                st.rerun()
            else:
                st.markdown(f'<div class="error-message">❌ {message}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def render_signup_form():
    """Render sign up form"""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="category-card">', unsafe_allow_html=True)
        st.markdown('<h2 class="subtitle-gradient">📝 Daftar Akun</h2>', unsafe_allow_html=True)
        
        new_user = st.text_input("👤 Buat Username")
        new_pass = st.text_input("🔒 Buat Password", type="password")
        
        if st.button("🎉 Daftar", key="signup_btn"):
            success, message = register_user(new_user, new_pass)
            if success:
                st.markdown(f'<div class="success-message">🎊 {message}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="warning-message">⚠️ {message}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
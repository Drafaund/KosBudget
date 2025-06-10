# main.py

import streamlit as st
import os
from dotenv import load_dotenv
import time
# Load environment variables
load_dotenv()

# Import modules
from utils.calculations import calculate_allocation
from styles.custom_css import apply_custom_css
from components.auth import render_auth_page
from utils.state_manager import SessionManager
from config.database import DatabaseManager
from pages.form_input import render_form_input

# Page configuration
st.set_page_config(
    page_title="KosBudget - Manajemen Keuangan Cerdas",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main application function"""
    
    # Apply custom CSS
    apply_custom_css()
    
    # Initialize session
    SessionManager.initialize_session()
    
    # Test database connection
    test_db_connection()
    
    # Routing
    if not SessionManager.is_authenticated():
        render_auth_page()
    else:
        render_dashboard()

      # Schedule allocation calculation
    if st.session_state.get('last_calculation', 0) < time.time() - 60:  # Every 60 seconds
        user_id = SessionManager.get_user_id()
        if user_id:
            calculate_allocation(user_id)
        st.session_state['last_calculation'] = time.time()  

def test_db_connection():
    """Test database connection dan tampilkan status"""
    if st.sidebar.button("🔧 Test Database Connection"):
        with st.spinner("Testing database connection..."):
            success, message = DatabaseManager.test_connection()
            if success:
                st.sidebar.success(f"✅ {message}")
            else:
                st.sidebar.error(f"❌ {message}")

def render_dashboard():
    """Render dashboard untuk user yang sudah login"""
    user_data = SessionManager.get_current_user()
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<h1 class="title-gradient">🏠 KosBudget Dashboard</h1>', unsafe_allow_html=True)
        st.markdown(f'<p style="color: white;">Selamat datang, **{user_data["username"]}**!</p>', unsafe_allow_html=True)
    
    with col2:
        if st.button("🚪 Logout", key="logout_btn"):
            SessionManager.clear_user_session()
            st.rerun()
    
    # Sidebar navigation
    st.sidebar.markdown('<h2 class="subtitle-gradient">📊 Menu Navigasi</h2>', unsafe_allow_html=True)
    
    menu_options = [
        "📈 Dashboard",
        "📝 Form Input",
        "⚙️ Settings",
        
    ]
    
    selected_menu = st.sidebar.selectbox("Pilih Menu", menu_options)
    
    # Content area
    if selected_menu == "📈 Dashboard":
        render_dashboard_content()
    elif selected_menu == "📝 Form Input":
        render_form_input()
    elif selected_menu == "⚙️ Settings":
        render_settings()

def render_dashboard_content():
    """Render dashboard content"""
    st.markdown('<h2 class="subtitle-gradient">📊 Dashboard Overview</h2>', unsafe_allow_html=True)
    
    # Metrics cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('''
            <div class="metric-card">
                <div class="metric-value">Rp 0</div>
                <div class="metric-label">Budget Bulan Ini</div>
            </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown('''
            <div class="metric-card">
                <div class="metric-value">Rp 0</div>
                <div class="metric-label">Total Pengeluaran</div>
            </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown('''
            <div class="metric-card">
                <div class="metric-value">Rp 0</div>
                <div class="metric-label">Sisa Budget</div>
            </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        st.markdown('''
            <div class="metric-card">
                <div class="metric-value">0</div>
                <div class="metric-label">Kategori Aktif</div>
            </div>
        ''', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Info section
    st.info("🚀 Dashboard ini akan menampilkan ringkasan keuangan Anda setelah Anda menambahkan budget dan pengeluaran.")

def render_settings():
    """Render settings page"""
    st.markdown('<h2 class="subtitle-gradient">⚙️ Pengaturan</h2>', unsafe_allow_html=True)
    
    user_data = SessionManager.get_current_user()
    
    # User info
    st.subheader("👤 Informasi Akun")
    st.write(f"**Username:** {user_data['username']}")
    st.write(f"**User ID:** {user_data['user_id']}")
    
    # Change password section
    st.subheader("🔒 Ubah Password")
    
    with st.form("change_password_form"):
        old_password = st.text_input("Password Lama", type="password")
        new_password = st.text_input("Password Baru", type="password")
        confirm_password = st.text_input("Konfirmasi Password Baru", type="password")
        
        submitted = st.form_submit_button("🔄 Ubah Password")
        
        if submitted:
            if not old_password or not new_password or not confirm_password:
                st.error("Semua field harus diisi!")
            elif new_password != confirm_password:
                st.error("Password baru dan konfirmasi tidak cocok!")
            else:
                from services.auth_service import AuthService
                success, message = AuthService.change_password(
                    user_data['user_id'], 
                    old_password, 
                    new_password
                )
                if success:
                    st.success(message)
                else:
                    st.error(message)

if __name__ == "__main__":
    main()
# utils/state_manager.py

import streamlit as st
from services.auth_service import AuthService

class SessionManager:
    """Manager untuk session state Streamlit"""
    
    @staticmethod
    def initialize_session():
        """Initialize session state variables"""
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        
        if 'user_data' not in st.session_state:
            st.session_state.user_data = None
        
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'auth'
    
    @staticmethod
    def set_user_session(user_data):
        """
        Set user session after successful login
        
        Args:
            user_data (dict): User data from database
        """
        st.session_state.authenticated = True
        st.session_state.user_data = user_data
        st.session_state.current_page = 'dashboard'
    
    @staticmethod
    def clear_user_session():
        """Clear user session (logout)"""
        st.session_state.authenticated = False
        st.session_state.user_data = None
        st.session_state.current_page = 'auth'
    
    @staticmethod
    def is_authenticated():
        """Check if user is authenticated"""
        return st.session_state.get('authenticated', False)
    
    @staticmethod
    def get_current_user():
        """Get current user data"""
        if SessionManager.is_authenticated():
            return st.session_state.get('user_data')
        return None
    
    @staticmethod
    def get_user_id():
        """Get current user ID"""
        user_data = SessionManager.get_current_user()
        if user_data:
            return user_data.get('user_id')
        return None
    
    @staticmethod
    def get_username():
        """Get current username"""
        user_data = SessionManager.get_current_user()
        if user_data:
            return user_data.get('username')
        return None

# Fungsi untuk kompatibilitas dengan kode yang sudah ada
def authenticate_user(username, password):
    """
    Authenticate user - wrapper untuk AuthService
    
    Args:
        username (str): Username
        password (str): Password
        
    Returns:
        tuple: (success, message)
    """
    success, message, user_data = AuthService.authenticate_user(username, password)
    
    if success:
        # Set session jika login berhasil
        SessionManager.set_user_session(user_data)
        return True, message
    else:
        return False, message

def register_user(username, password):
    """
    Register new user - wrapper untuk AuthService
    
    Args:
        username (str): Username
        password (str): Password
        
    Returns:
        tuple: (success, message)
    """
    return AuthService.register_user(username, password)

def logout_user():
    """Logout current user"""
    SessionManager.clear_user_session()
    return True, "Logout berhasil"

def get_current_user_info():
    """Get current user information"""
    return SessionManager.get_current_user()

# Initialize session saat module di-import
SessionManager.initialize_session()
# styles/custom_css.py

CUSTOM_CSS = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        font-family: 'Inter', sans-serif;
        min-height: 100vh;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    .sidebar .sidebar-content {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
    }
    
    .css-18ni7ap.e8zbici2 {
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 2rem;
        margin-bottom: 2rem;
    }
    
    .stButton>button {
        border-radius: 12px;
        padding: 0.75rem 2rem;
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        color: white;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    .sidebar .stButton>button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        width: 100%;
        margin-bottom: 0.5rem;
    }
    
    .auth-button {
        background: linear-gradient(45deg, #11998e, #38ef7d) !important;
    }
    
    .delete-button {
        background: linear-gradient(45deg, #ff416c, #ff4b2b) !important;
    }
    
    .stTextInput>div>div>input {
        border-radius: 12px;
        border: 2px solid #e1e5e9;
        padding: 0.75rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .stNumberInput>div>div>input {
        border-radius: 12px;
        border: 2px solid #e1e5e9;
        padding: 0.75rem;
    }
    
    .stSelectbox>div>div>select {
        border-radius: 12px;
        border: 2px solid #e1e5e9;
        padding: 0.75rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        font-weight: 500;
    }
    
    .decision-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 12px;
        color: white;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
    }
    
    .success-message {
        background: linear-gradient(45deg, #11998e, #38ef7d);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
    }
    
    .warning-message {
        background: linear-gradient(45deg, #f093fb, #f5576c);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
    }
    
    .error-message {
        background: linear-gradient(45deg, #ff416c, #ff4b2b);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
    }
    
    .title-gradient {
        background: linear-gradient(45deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .subtitle-gradient {
        background: linear-gradient(45deg, #11998e, #38ef7d);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 600;
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .avatar {
        float: right;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        margin-top: -70px;
        margin-right: 20px;
        border: 3px solid #667eea;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stProgress .stProgress-bar {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        border-radius: 10px;
    }
    
    .dataframe {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    .stSlider>div>div>div>div {
        background: linear-gradient(45deg, #667eea, #764ba2);
    }
    </style>
"""

def get_custom_css():
    """
    Mengembalikan CSS kustom untuk aplikasi Streamlit
    
    Returns:
        str: String CSS yang sudah diformat dalam tag HTML
    """
    return CUSTOM_CSS

def apply_custom_css():
    """
    Mengaplikasikan CSS kustom ke aplikasi Streamlit menggunakan st.markdown
    Fungsi ini bisa dipanggil langsung untuk menerapkan styling
    """
    import streamlit as st
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
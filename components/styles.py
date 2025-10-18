import streamlit as st

def apply_custom_styles():
    """Aplica CSS personalizado à aplicação"""
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        }
        .main-header {
            font-size: 2.5rem;
            color: #00d4ff;
            text-align: center;
            margin-bottom: 1rem;
        }
        .sub-header {
            font-size: 1.2rem;
            color: #a8dadc;
            text-align: center;
            margin-bottom: 2rem;
        }
        .specs-card {
            background: linear-gradient(135deg, #2d4059 0%, #1f3044 100%);
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 4px solid #00d4ff;
            margin: 0.5rem 0;
            border: 1px solid #3d5a73;
        }
        .results-card {
            background: linear-gradient(135deg, #2d4059 0%, #1f3044 100%);
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 4px solid #00d4ff;
            margin: 0.5rem 0;
            border: 1px solid #3d5a73;
        }
        .result-card {
            background: linear-gradient(135deg, #3d5a80 0%, #2c4563 100%);
            padding: 1rem;
            border-radius: 8px;
            border: 2px solid #00d4ff;
            text-align: center;
            box-shadow: 0 4px 8px rgba(0, 212, 255, 0.2);
            margin: 0.5rem 0;
        }
        .result-card h3 {
            color: #00d4ff;
            margin-bottom: 0.5rem;
            font-size: 1.1rem;
        }
        .result-card h2 {
            color: #e0fbfc;
            margin: 0.5rem 0;
            font-size: 1.8rem;
        }
        .warning {
            background-color: #3d4f2f;
            border: 1px solid #6b8e23;
            border-radius: 5px;
            padding: 0.75rem;
            margin: 0.5rem 0;
            color: #d4edda;
        }
        .alert-warning {
            background-color: #5a3a1a;
            border: 1px solid #ff9800;
            border-radius: 5px;
            padding: 0.75rem;
            margin: 0.5rem 0;
            color: #ffd60a;
        }
        .section-title {
            color: #00d4ff;
            border-bottom: 2px solid #00d4ff;
            padding-bottom: 0.5rem;
            margin-bottom: 1rem;
        }
        div[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1a1a2e 0%, #0f3460 100%);
        }
        div[data-testid="stSidebar"] * {
            color: #e0fbfc !important;
        }
        label {
            color: #a8dadc !important;
        }
        .stMarkdown {
            color: #e0fbfc;
        }
        p {
            color: #e0fbfc;
        }
        small {
            color: #a8dadc;
        }
        h1, h2, h3, h4 {
            color: #00d4ff !important;
        }
        .stTabs [data-baseweb="tab-list"] {
            background-color: #2d4059;
        }
        .stTabs [data-baseweb="tab"] {
            color: #a8dadc;
        }
        .stTabs [aria-selected="true"] {
            color: #00d4ff !important;
            border-bottom-color: #00d4ff !important;
        }
        .pipe-card {
            background: linear-gradient(135deg, #2a4556 0%, #1e3542 100%);
            padding: 1rem;
            border-radius: 8px;
            border: 2px solid #4ecdc4;
            margin: 0.5rem 0;
        }
    </style>
    """, unsafe_allow_html=True)

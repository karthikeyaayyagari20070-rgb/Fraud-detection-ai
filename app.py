import streamlit as st
from PIL import Image
import pandas as pd
import io

# Set page config
st.set_page_config(
    page_title="Banking Fraud Detection System",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .risk-high {
        background-color: #ffebee;
        padding: 1rem;
        border-left: 5px solid #f44336;
        border-radius: 5px;
    }
    .risk-medium {
        background-color: #fff9c4;
        padding: 1rem;
        border-left: 5px solid #ff9800;
        border-radius: 5px;
    }
    .risk-low {
        background-color: #e8f5e9;
        padding: 1rem;
        border-left: 5px solid #4caf50;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'Home'

# Sidebar navigation
st.sidebar.title("🔒 Fraud Detection")
st.sidebar.markdown("---")

pages = {
    "🏠 Home": "Home",
    "📄 Document Tampering": "Document Tampering",
    "✍️ Signature Fraud": "Signature Fraud",
    "🆔 Aadhaar Verification": "Aadhaar Verification",
    "💳 PAN Verification": "PAN Verification",
    "👤 KYC Processing": "KYC Processing",
    "💰 Transaction Analysis": "Transaction Analysis"
}

for label, page_name in pages.items():
    if st.sidebar.button(label, use_container_width=True):
        st.session_state.page = page_name

st.sidebar.markdown("---")
st.sidebar.info("""
**Banking Fraud Detection System**

AI-powered fraud detection for:
- Document verification
- Signature analysis
- Identity validation
- Transaction monitoring
""")

# Main content area
if st.session_state.page == "Home":
    st.markdown('<div class="main-header">🔒 Banking Fraud Detection System</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### Welcome to the AI-Powered Banking Fraud Detection System
    
    This comprehensive fraud detection platform helps identify and prevent banking fraud through advanced AI analysis and pattern recognition.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        #### 📄 Document Analysis
        - **Document Tampering Detection**: AI-powered analysis to detect alterations and forgery
        - **Visual Inspection**: Identifies inconsistencies, artifacts, and manipulation signs
        """)
    
    with col2:
        st.markdown("""
        #### 🆔 Identity Verification
        - **Aadhaar Verification**: Format validation and visual authenticity checks
        - **PAN Verification**: Structure validation and document analysis
        - **KYC Processing**: Automated information extraction from ID documents
        """)
    
    with col3:
        st.markdown("""
        #### 💰 Transaction Monitoring
        - **Pattern Analysis**: Detect unusual transaction patterns
        - **Anomaly Detection**: ML-based identification of suspicious activity
        - **Risk Scoring**: Comprehensive fraud risk assessment
        """)
    
    st.markdown("---")
    st.markdown("""
    ### 🚀 Getting Started
    
    Select a feature from the sidebar to begin fraud detection analysis:
    1. **Document Tampering**: Upload documents to check for manipulation
    2. **Signature Fraud**: Compare signatures to detect forgery
    3. **Aadhaar/PAN Verification**: Validate Indian identity documents
    4. **KYC Processing**: Extract and validate customer information
    5. **Transaction Analysis**: Upload transaction data to detect anomalies
    """)
    
    st.success("✅ System is ready. Select a feature from the sidebar to begin.")

elif st.session_state.page == "Document Tampering":
    from pages import document_tampering
    document_tampering.show()

elif st.session_state.page == "Signature Fraud":
    from pages import signature_fraud
    signature_fraud.show()

elif st.session_state.page == "Aadhaar Verification":
    from pages import aadhaar_verification
    aadhaar_verification.show()

elif st.session_state.page == "PAN Verification":
    from pages import pan_verification
    pan_verification.show()

elif st.session_state.page == "KYC Processing":
    from pages import kyc_processing
    kyc_processing.show()

elif st.session_state.page == "Transaction Analysis":
    from pages import transaction_analysis_page
    transaction_analysis_page.show()

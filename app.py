import streamlit as st
import pandas as pd
import joblib
import re
import time

st.set_page_config(
    page_title="PhishGuard | AI Detector",
    page_icon="🛡️",
    layout="wide"
)

st.markdown("""
    <style>
    /* Main Background - Deep Slate/Navy Gradient */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #e2e8f0;
    }
    
    /* Headers - Clean Sans-Serif */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        color: #f8fafc;
        font-weight: 700;
    }
    
    /* Input Field - Dark Glass */
    .stTextInput > div > div > input {
        background-color: rgba(30, 41, 59, 0.8);
        color: #f1f5f9;
        border: 1px solid #475569;
        border-radius: 8px;
        padding: 12px;
    }
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.3);
    }
    
    /* Buttons - Professional Gradient */
    .stButton > button {
        background: linear-gradient(to right, #3b82f6, #2563eb);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(to right, #2563eb, #1d4ed8);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        transform: translateY(-1px);
    }
    
    /* Sidebar - Semi-transparent Dark */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.95);
        border-right: 1px solid #334155;
    }
    
    /* Metric Cards & Expanders - subtle separation */
    div[data-testid="metric-container"], .streamlit-expanderHeader {
        background-color: rgba(30, 41, 59, 0.5);
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 10px;
    }
    
    /* Status Colors (Subtle, not Neon) */
    .status-safe { color: #10b981; }      /* Emerald Green */
    .status-warn { color: #f59e0b; }      /* Amber */
    .status-danger { color: #ef4444; }    /* Red */
    
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    try:
        return joblib.load("phishing_model.pkl")
    except FileNotFoundError:
        st.error("Model file not found! Please run the training script first.")
        return None

model = load_model()

def extract_features(url):
    features = {}
    features['length_url'] = len(url)
    features['nb_dots'] = url.count('.')
    features['nb_hyphens'] = url.count('-')
    features['nb_at'] = url.count('@')
    features['nb_slash'] = url.count('/')
    features['nb_www'] = 1 if 'www' in url else 0
    features['https_token'] = 1 if 'https' in url else 0
    
    ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    features['ip'] = 1 if re.search(ip_pattern, url) else 0
    return features

def keyword_analysis(url):
    suspicious_keywords = [
        'login', 'secure', 'account', 'update', 'banking', 
        'verify', 'confirm', 'wallet', 'signin', 'support'
    ]
    found_keywords = [word for word in suspicious_keywords if word in url.lower()]
    return found_keywords

col1, col2 = st.columns([1, 6])
with col1:
    st.markdown("<div style='font-size: 60px;'>🛡️</div>", unsafe_allow_html=True)
with col2:
    st.title("PhishGuard AI")
    st.markdown("##### Intelligent Threat Detection System")

st.markdown("---")

with st.sidebar:
    st.header("⚙️ Settings")
    
    st.subheader("Analysis Sensitivity")
    sensitivity = st.slider("Risk Threshold", 0.1, 1.0, 0.3, 0.05, help="Adjust how strict the AI should be.")
    
    st.markdown("---")
    st.info("""
    **System Status:** 🟢 Online
    
    **Engine:** Hybrid (AI + Heuristic)
    **Version:** 2.2.0 Stable
    """)

st.markdown("### 🔍 URL Analysis")

if 'url_input' not in st.session_state:
    st.session_state.url_input = ""

url_input = st.text_input(
    "Enter Target URL", 
    value=st.session_state.url_input,
    placeholder="https://example.com/page",
    label_visibility="collapsed"
)

if st.button("🚀 Analyze Now", type="primary"):
    if not url_input:
        st.warning("Please enter a URL first.")
    elif model is None:
        st.error("Model not loaded.")
    else:
        with st.spinner("Analyzing threat vectors..."):
            time.sleep(1) 
            
            features = extract_features(url_input)
            input_df = pd.DataFrame([features])
            ai_phishing_prob = model.predict_proba(input_df)[0][1]
            found_keywords = keyword_analysis(url_input)
            
            final_score = ai_phishing_prob
            risk_factor = 0.35 if found_keywords else 0
            final_score += risk_factor
            adjusted_score = min(final_score / sensitivity, 1.0)
            
            st.markdown("---")
            
            res_col1, res_col2 = st.columns([3, 1])
            
            with res_col1:
                if adjusted_score > 0.60:
                    st.markdown("### <span class='status-danger'>🚫 CRITICAL THREAT DETECTED</span>", unsafe_allow_html=True)
                    st.write(f"The URL **{url_input}** matches known phishing patterns.")
                elif adjusted_score > 0.30:
                    st.markdown("### <span class='status-warn'>⚠️ POTENTIAL RISK</span>", unsafe_allow_html=True)
                    st.write("This site shows suspicious characteristics. Proceed with caution.")
                else:
                    st.markdown("### <span class='status-safe'>✅ SAFE SITE</span>", unsafe_allow_html=True)
                    st.write("No malicious indicators found.")

            with res_col2:
                st.metric("Risk Score", f"{adjusted_score*100:.1f}%")
                st.progress(adjusted_score)

            if found_keywords:
                st.warning(f"**Keywords Detected:** {', '.join(found_keywords)}")

            with st.expander("View Technical Telemetry"):
                st.dataframe(pd.DataFrame(list(features.items()), columns=['Feature', 'Value']))
                
                m1, m2 = st.columns(2)
                m1.metric("Base AI Probability", f"{ai_phishing_prob:.4f}")
                m2.metric("Heuristic Adjustment", f"+{risk_factor:.2f}")
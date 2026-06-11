import base64
from pathlib import Path
import streamlit as st

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="OtakuAI",
    page_icon="🎌",
    layout="wide"
)

# Helper to load image as base64
def get_base64_image(image_path):
    try:
        path = Path(image_path)
        if path.exists():
            with open(path, "rb") as image_file:
                encoded = base64.b64encode(image_file.read()).decode()
            return f"data:image/png;base64,{encoded}"
    except Exception:
        pass
    return ""

banner_base64 = get_base64_image("assets/otakuai_banner.png")

# --------------------------------------------------
# CUSTOM CSS & THEME OVERRIDES
# --------------------------------------------------

st.markdown("""
<style>

/* Reduce default padding for better above-the-fold visibility */
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 1.5rem !important;
}

.main {
    padding-top: 0rem;
}

/* Animations */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(15px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes gradientShift {
    0% {
        background-position: 0% 50%;
    }
    50% {
        background-position: 100% 50%;
    }
    100% {
        background-position: 0% 50%;
    }
}

@keyframes floatAnimation {
    0% {
        transform: translateY(0px);
    }
    100% {
        transform: translateY(-4px);
    }
}

/* Hero Section with Animated Gradient Border */
.hero-container {
    position: relative;
    width: 100%;
    height: 260px;
    border-radius: 20px;
    margin-bottom: 1.5rem;
    padding: 2px; /* acts as border size */
    background: linear-gradient(
        90deg,
        #00f5ff,
        #a855f7,
        #ec4899,
        #00f5ff
    );
    background-size: 300% 300%;
    animation: fadeIn 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards, gradientShift 10s ease infinite;
    box-shadow: 0 8px 32px 0 rgba(168, 85, 247, 0.2);
}

.hero-inner {
    position: relative;
    width: 100%;
    height: 100%;
    border-radius: 18px;
    background: rgba(13, 13, 21, 0.85);
    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px);
    padding: 1.5rem 2rem;
    display: grid;
    grid-template-columns: 1.3fr 1fr 1fr;
    gap: 1.5rem;
    align-items: center;
    box-sizing: border-box;
}

/* Hero Left Column */
.hero-left-col {
    display: flex;
    flex-direction: column;
    justify-content: center;
    color: #ffffff;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.85);
}

.hero-title-wrapper {
    display: flex;
    align-items: center;
    gap: 0.6rem;
}

.hero-emoji {
    font-size: 2rem;
}

.hero-title {
    font-size: 2.4rem !important;
    font-weight: 800 !important;
    margin: 0 !important;
    color: #ffffff !important;
    letter-spacing: -0.02rem;
    line-height: 1.1 !important;
}

.hero-subtitle {
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    margin: 0.2rem 0 0 0 !important;
    color: #00f5ff !important;
    text-shadow: 0 0 8px rgba(0, 245, 255, 0.25);
    letter-spacing: 0.02rem;
}

.hero-description {
    font-size: 0.85rem !important;
    font-weight: 400 !important;
    margin-top: 0.6rem !important;
    margin-bottom: 0 !important;
    color: rgba(255, 255, 255, 0.7) !important;
    line-height: 1.4 !important;
}

/* Hero Center Column */
.hero-center-col {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
}

.hero-banner-img {
    max-height: 180px;
    width: 100%;
    object-fit: cover;
    border-radius: 14px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}

/* Hero Right Column (GIF Card) */
.hero-right-col {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
}

.gif-glass-card {
    position: relative;
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(0, 245, 255, 0.2);
    border-radius: 18px;
    padding: 4px;
    box-shadow: 0 8px 32px 0 rgba(0, 245, 255, 0.15), 
                0 0 10px rgba(168, 85, 247, 0.1);
    animation: floatAnimation 4s ease-in-out infinite alternate;
    transition: all 0.3s ease;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 180px;
    width: 100%;
}

.gif-glass-card:hover {
    transform: scale(1.02) translateY(-4px);
    box-shadow: 0 12px 40px 0 rgba(0, 245, 255, 0.3), 
                0 0 15px rgba(168, 85, 247, 0.25);
    border-color: rgba(0, 245, 255, 0.5);
}

.hero-gif {
    height: 100%;
    width: 100%;
    object-fit: cover;
    border-radius: 14px;
}

/* KPI Cards Layout */
.kpi-container {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1.25rem;
    margin-bottom: 2rem;
}

.kpi-card {
    background: rgba(20, 20, 35, 0.65);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 1.25rem 1rem;
    text-align: center;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    transition: all 0.3s ease;
    opacity: 0;
}

.kpi-card:nth-child(1) { animation: fadeIn 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.1s both; }
.kpi-card:nth-child(2) { animation: fadeIn 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.2s both; }
.kpi-card:nth-child(3) { animation: fadeIn 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.3s both; }
.kpi-card:nth-child(4) { animation: fadeIn 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.4s both; }

.kpi-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 30px rgba(0, 245, 255, 0.2), 
                0 0 15px rgba(168, 85, 247, 0.15);
    border-color: rgba(0, 245, 255, 0.5);
    background: rgba(0, 245, 255, 0.03);
}

.kpi-label {
    font-size: 0.75rem;
    color: rgba(255, 255, 255, 0.6) !important;
    text-transform: uppercase;
    letter-spacing: 0.1rem;
    margin-bottom: 0.35rem;
    font-weight: 600;
}

.kpi-value {
    font-size: 1.8rem;
    font-weight: 800;
    color: #00f5ff !important;
    text-shadow: 0 0 8px rgba(0, 245, 255, 0.25);
}

/* Feature Cards */
.feature-card {
    padding: 1.5rem;
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    background: rgba(20, 20, 35, 0.65);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    min-height: 200px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    transition: all 0.3s ease;
    opacity: 0;
    color: rgba(255, 255, 255, 0.85) !important;
}

/* Staggered card fade-in */
.card-1 { animation: fadeIn 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.3s both; }
.card-2 { animation: fadeIn 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.4s both; }
.card-3 { animation: fadeIn 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.5s both; }

.feature-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 30px rgba(236, 72, 153, 0.2), 
                0 0 15px rgba(168, 85, 247, 0.15);
    border-color: rgba(236, 72, 153, 0.5);
    background: rgba(236, 72, 153, 0.03);
}

.feature-card h2 {
    margin-top: 0 !important;
    font-size: 1.45rem !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    letter-spacing: -0.01rem;
}

.feature-card p, .feature-card li {
    color: rgba(255, 255, 255, 0.75) !important;
}

/* Quote Box */
.quote-box {
    padding: 1.5rem;
    border-radius: 16px;
    background: rgba(20, 20, 35, 0.65);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-left: 5px solid #a855f7;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    border-right: 1px solid rgba(255, 255, 255, 0.08);
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    color: #ffffff !important;
}

.quote-box p {
    color: rgba(255, 255, 255, 0.85) !important;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HERO SECTION
# --------------------------------------------------

st.markdown(f"""
<div class="hero-container">
    <div class="hero-inner">
        <!-- Column 1: Info -->
        <div class="hero-left-col">
            <div class="hero-title-wrapper">
                <span class="hero-emoji">🎌</span>
                <h1 class="hero-title">OtakuAI</h1>
            </div>
            <p class="hero-subtitle">Anime Review Intelligence Platform</p>
            <p class="hero-description">
                Analyze anime reviews using Natural Language Processing, Machine Learning, and Interactive Analytics.
            </p>
        </div>
        <!-- Column 2: Banner Image -->
        <div class="hero-center-col">
            <img src="{banner_base64}" class="hero-banner-img" alt="OtakuAI Banner" />
        </div>
        <!-- Column 3: Cyberpunk GIF -->
        <div class="hero-right-col">
            <div class="gif-glass-card">
                <img class="hero-gif" src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcHY0ZThpcjdnZGl2czJycW93MTM4ZG4xdDg0YXJheGV3Y3o3dWZycSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/vCFw1RYAkJgyXxlvGz/giphy.gif" alt="Cyberpunk GIF" />
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------

st.markdown("""
<div class="kpi-container">
    <div class="kpi-card">
        <div class="kpi-label">Reviews</div>
        <div class="kpi-value">1,490</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Accuracy</div>
        <div class="kpi-value">82.6%</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Features</div>
        <div class="kpi-value">1,000</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Model</div>
        <div class="kpi-value">LogReg</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# FEATURE SECTION
# --------------------------------------------------

st.subheader("🚀 Platform Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
<div class="feature-card card-1">

## 🎭 Sentiment Predictor

Input any anime review and receive:
- Sentiment prediction
- Confidence score
- Real-time inference
- NLP preprocessing

</div>
""", unsafe_allow_html=True)

with col2:
    st.markdown("""
<div class="feature-card card-2">

## 📈 Model Insights

Understand how the model works:
- Feature importance
- Positive indicators
- Negative indicators
- Explainable AI

</div>
""", unsafe_allow_html=True)

with col3:
    st.markdown("""
<div class="feature-card card-3">

## 📊 Dataset Analytics

Explore the dataset:
- Sentiment distribution
- Review statistics
- Review length analysis
- Dataset overview

</div>
""", unsafe_allow_html=True)

st.divider()

# --------------------------------------------------
# WORKFLOW & TECH STACK
# --------------------------------------------------

col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("⚙️ ML Pipeline")
    st.markdown("""
```text
Anime Reviews
      ↓
Text Cleaning
      ↓
TF-IDF Vectorization
      ↓
Logistic Regression
      ↓
Sentiment Prediction
      ↓
Interactive Dashboard
```
""")

with col_right:
    st.subheader("🛠️ Tech Stack")
    
    col_tech1, col_tech2 = st.columns(2)
    with col_tech1:
        st.markdown("""
**Machine Learning**
- Python
- Pandas
- NumPy
- Scikit-Learn
- NLTK
""")
    with col_tech2:
        st.markdown("""
**Application Layer**
- Streamlit
- Plotly
- WordCloud
- Matplotlib
""")

st.divider()

# --------------------------------------------------
# ANIME QUOTE
# --------------------------------------------------

st.markdown("""
<div class="quote-box">
🌸 Inspiration

"The world isn't perfect. But it's there for us, doing the best it can."

— Roy Mustang, Fullmetal Alchemist
</div>
""", unsafe_allow_html=True)

st.write("")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.caption(
    "OtakuAI • Anime Review Sentiment Intelligence Platform • Built with NLP & Machine Learning"
)
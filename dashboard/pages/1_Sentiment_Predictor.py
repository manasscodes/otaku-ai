import streamlit as st
import joblib
import plotly.graph_objects as go

# -----------------------------
# Page Config
# -----------------------------

st.set_page_config(
    page_title="Sentiment Predictor",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------
# Load Artifacts
# -----------------------------

@st.cache_resource
def load_artifacts():
    model = joblib.load("artifacts/sentiment_model.pkl")
    vectorizer = joblib.load("artifacts/tfidf_vectorizer.pkl")
    return model, vectorizer

try:
    model, vectorizer = load_artifacts()
    feature_names = vectorizer.get_feature_names_out()
except Exception as e:
    st.error(f"Error loading model artifacts: {e}")
    st.stop()

# -----------------------------
# CUSTOM CSS & THEMING
# -----------------------------

st.markdown("""
<style>
/* Reduce default padding */
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
}

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

/* Page containers fade in */
div[data-testid="stColumn"] {
    animation: fadeIn 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.predictor-gif-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    min-height: 250px;
    padding: 10px;
}

.predictor-gif {
    height: 250px;
    max-height: 280px;
    border-radius: 15px;
    border: 1px solid rgba(255, 0, 127, 0.4);
    box-shadow: 0 0 25px rgba(255, 0, 127, 0.25);
    object-fit: contain;
    width: 100%;
    transition: all 0.3s ease;
}

.predictor-gif:hover {
    transform: translateY(-5px);
    box-shadow: 0 0 30px rgba(255, 0, 127, 0.45);
    border-color: rgba(255, 0, 127, 0.7);
}

/* Style output alerts */
.stAlert {
    border-radius: 12px !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    background: rgba(20, 20, 35, 0.6) !important;
    backdrop-filter: blur(10px) !important;
    -webkit-backdrop-filter: blur(10px) !important;
}

/* Glassmorphism metric container */
div[data-testid="stMetricValue"] {
    font-weight: 800 !important;
    color: #00f0ff !important;
    text-shadow: 0 0 8px rgba(0, 240, 255, 0.3);
}

/* Glassmorphism info card */
.info-card {
    background: rgba(0, 240, 255, 0.04) !important;
    border: 1px solid rgba(0, 240, 255, 0.15) !important;
    border-radius: 12px;
    padding: 0.8rem 1.2rem;
    margin-top: 0.75rem;
    margin-bottom: 1.25rem;
    font-size: 0.9rem;
    color: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
}

.no-signals-text {
    font-size: 0.9rem;
    color: rgba(255, 255, 255, 0.45);
    font-style: italic;
    margin-top: 0.5rem;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# UI Layout
# -----------------------------

st.title("🤖 Anime Review Sentiment Predictor")
st.write("Input any anime review below and the machine learning model will classify the sentiment in real-time.")

col_left, col_right = st.columns([3, 2], gap="large")

with col_left:
    review = st.text_area(
        "Enter an anime review:",
        placeholder="Type or paste review content here...",
        height=200
    )
    
    predict_clicked = st.button("Predict Sentiment", use_container_width=True)
    
    if predict_clicked:
        if review.strip() == "":
            st.warning("Please enter a review text to predict.")
        else:
            # Predict
            vectorized_review = vectorizer.transform([review])
            prediction = model.predict(vectorized_review)[0]
            confidence = model.predict_proba(vectorized_review).max()
            
            st.markdown("### 📊 Inference Results")
            
            if prediction == "Positive":
                st.success(f"🎉 **Prediction:** Positive Sentiment")
            else:
                st.error(f"😬 **Prediction:** Negative Sentiment")
                
            st.metric(
                label="Confidence Score",
                value=f"{confidence:.2%}"
            )
            
            # -----------------------------
            # EXPLAINABLE AI (XAI)
            # -----------------------------
            
            # Extract TF-IDF contributions
            coo = vectorized_review.tocoo()
            coef = model.coef_[0]
            
            contributions = []
            for col_idx, tfidf_val in zip(coo.col, coo.data):
                word = feature_names[col_idx]
                coefficient = coef[col_idx]
                contribution = tfidf_val * coefficient
                contributions.append((word, contribution))
                
            # Filter positive and negative signals
            positive_signals = [item for item in contributions if item[1] > 0]
            negative_signals = [item for item in contributions if item[1] < 0]
            
            # Sort by absolute contribution magnitude
            positive_signals.sort(key=lambda x: abs(x[1]), reverse=True)
            negative_signals.sort(key=lambda x: abs(x[1]), reverse=True)
            
            top_positive = positive_signals[:5]
            top_negative = negative_signals[:5]
            
            st.markdown("---")
            st.subheader("🔍 Explainable AI (Local Feature Attributions)", help="Contribution = TF-IDF value × Logistic Regression coefficient")
            
            # Info Card
            st.markdown("""
            <div class="info-card">
                💡 <b>Explainable AI</b>: These words had the strongest influence on the model's decision.
            </div>
            """, unsafe_allow_html=True)
            
            # Attributions columns
            att_col1, att_col2 = st.columns(2)
            
            # Helper to create a plotly chart
            def create_attribution_chart(signals, color):
                if not signals:
                    return None
                
                # Reverse signals for Plotly y-axis ordering to show highest contribution at the top
                sorted_signals = list(reversed(signals))
                words = [item[0] for item in sorted_signals]
                scores = [item[1] for item in sorted_signals]
                
                fig = go.Figure(go.Bar(
                    x=scores,
                    y=words,
                    orientation='h',
                    marker_color=color,
                    hovertemplate='<b>%{y}</b><br>Contribution: %{x:+.4f}<extra></extra>',
                    text=[f"{s:+.3f}" for s in scores],
                    textposition='outside',
                    cliponaxis=False
                ))
                
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=80, r=45, t=10, b=10),
                    height=200,
                    xaxis=dict(
                        showgrid=True,
                        gridcolor='rgba(255,255,255,0.05)',
                        zeroline=True,
                        zerolinecolor='rgba(255,255,255,0.2)',
                        tickfont=dict(color='rgba(255,255,255,0.5)', size=10),
                        showticklabels=True
                    ),
                    yaxis=dict(
                        tickfont=dict(color='#ffffff', size=12),
                        showgrid=False
                    ),
                    showlegend=False
                )
                return fig

            with att_col1:
                st.markdown("##### ✅ Positive Signals")
                if top_positive:
                    # Ranked list text
                    list_html = "".join([
                        f'<div style="margin-bottom:0.4rem; font-size:0.95rem;"><b>#{i+1}</b> <code style="color:#2ecc71; background:rgba(46,204,113,0.1); padding:2px 6px; border-radius:4px;">{word}</code> <b>({score:+.3f})</b></div>'
                        for i, (word, score) in enumerate(top_positive)
                    ])
                    st.markdown(list_html, unsafe_allow_html=True)
                    
                    # Horizontal Plotly Bar Chart
                    fig_pos = create_attribution_chart(top_positive, "#2ecc71")
                    if fig_pos:
                        st.plotly_chart(fig_pos, use_container_width=True, config={'displayModeBar': False})
                else:
                    st.markdown('<div class="no-signals-text">No positive signals detected in review</div>', unsafe_allow_html=True)
                    
            with att_col2:
                st.markdown("##### ❌ Negative Signals")
                if top_negative:
                    # Ranked list text
                    list_html = "".join([
                        f'<div style="margin-bottom:0.4rem; font-size:0.95rem;"><b>#{i+1}</b> <code style="color:#e74c3c; background:rgba(231,76,60,0.1); padding:2px 6px; border-radius:4px;">{word}</code> <b>({score:.3f})</b></div>'
                        for i, (word, score) in enumerate(top_negative)
                    ])
                    st.markdown(list_html, unsafe_allow_html=True)
                    
                    # Horizontal Plotly Bar Chart
                    fig_neg = create_attribution_chart(top_negative, "#e74c3c")
                    if fig_neg:
                        st.plotly_chart(fig_neg, use_container_width=True, config={'displayModeBar': False})
                else:
                    st.markdown('<div class="no-signals-text">No negative signals detected in review</div>', unsafe_allow_html=True)

with col_right:
    st.markdown("""
    <div class="predictor-gif-container">
        <img class="predictor-gif" src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdndidDl6YWlmcjlzOGhtcDhzeDBsdWJyZTk5OWp6OTloeXZhYTNtNCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/tcKnSDeltmpKxslv8r/giphy.gif" alt="Anime Predictor GIF" />
    </div>
    """, unsafe_allow_html=True)
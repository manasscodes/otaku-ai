import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Model Insights",
    page_icon="📈",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

coef_df = pd.read_csv(
    "data/processed/feature_importance.csv"
)

top_positive = (
    coef_df
    .sort_values("weight", ascending=False)
    .head(10)
)

top_negative = (
    coef_df
    .sort_values("weight", ascending=True)
    .head(10)
)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("📈 Model Insights")

st.markdown("""
Understand how the Logistic Regression model makes decisions by exploring
the most influential words driving positive and negative sentiment predictions.
""")

st.divider()

# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Features Analyzed",
        f"{len(coef_df):,}"
    )

with col2:
    st.metric(
        "Strongest Positive",
        top_positive.iloc[0]["word"]
    )

with col3:
    st.metric(
        "Strongest Negative",
        top_negative.iloc[0]["word"]
    )

st.divider()

# --------------------------------------------------
# TABLES
# --------------------------------------------------

left, right = st.columns(2)

with left:
    st.subheader("✅ Top Positive Words")

    st.dataframe(
        top_positive.reset_index(drop=True),
        use_container_width=True,
        hide_index=True
    )

with right:
    st.subheader("❌ Top Negative Words")

    st.dataframe(
        top_negative.reset_index(drop=True),
        use_container_width=True,
        hide_index=True
    )

st.divider()

# --------------------------------------------------
# POSITIVE CHART
# --------------------------------------------------

st.subheader("🚀 Positive Feature Importance")

positive_chart = px.bar(
    top_positive.sort_values("weight"),
    x="weight",
    y="word",
    orientation="h",
    text="weight",
    color="weight"
)

positive_chart.update_layout(
    height=500,
    xaxis_title="Coefficient Weight",
    yaxis_title="Word",
    coloraxis_showscale=False
)

positive_chart.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside"
)

st.plotly_chart(
    positive_chart,
    use_container_width=True
)

# --------------------------------------------------
# NEGATIVE CHART
# --------------------------------------------------

st.subheader("⚠️ Negative Feature Importance")

negative_chart = px.bar(
    top_negative.sort_values("weight"),
    x="weight",
    y="word",
    orientation="h",
    text="weight",
    color="weight"
)

negative_chart.update_layout(
    height=500,
    xaxis_title="Coefficient Weight",
    yaxis_title="Word",
    coloraxis_showscale=False
)

negative_chart.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside"
)

st.plotly_chart(
    negative_chart,
    use_container_width=True
)

# --------------------------------------------------
# INSIGHT BOX
# --------------------------------------------------

st.divider()

st.subheader("🧠 Model Interpretation")

st.info(
    """
    Logistic Regression assigns a coefficient weight to every word.

    • Positive coefficients increase the likelihood of a Positive prediction.

    • Negative coefficients increase the likelihood of a Negative prediction.

    • Larger absolute values indicate stronger influence on the model's decision.
    """
)
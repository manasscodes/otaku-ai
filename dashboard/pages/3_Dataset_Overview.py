import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Dataset Overview",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

df = pd.read_csv("data/processed/anime_reviews_processed.csv")

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("📊 Dataset Overview")

st.markdown("""
Explore the anime review dataset used to train OtakuAI.
""")

st.divider()

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

total_reviews = len(df)

positive_reviews = (
    df["binary_sentiment"] == "Positive"
).sum()

negative_reviews = (
    df["binary_sentiment"] == "Negative"
).sum()

avg_review_length = int(
    df["review_length"].mean()
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Reviews",
        f"{total_reviews:,}"
    )

with col2:
    st.metric(
        "Positive Reviews",
        f"{positive_reviews:,}"
    )

with col3:
    st.metric(
        "Negative Reviews",
        f"{negative_reviews:,}"
    )

with col4:
    st.metric(
        "Avg Review Length",
        f"{avg_review_length:,}"
    )

st.divider()

# --------------------------------------------------
# SENTIMENT DISTRIBUTION
# --------------------------------------------------

st.subheader("📈 Sentiment Distribution")

sentiment_counts = (
    df["binary_sentiment"]
    .value_counts()
    .reset_index()
)

sentiment_counts.columns = [
    "Sentiment",
    "Count"
]

fig = px.bar(
    sentiment_counts,
    x="Sentiment",
    y="Count",
    text="Count",
    color="Sentiment",
    title="Binary Sentiment Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# REVIEW LENGTH DISTRIBUTION
# --------------------------------------------------

st.subheader("📝 Review Length Distribution")

fig = px.histogram(
    df,
    x="review_length",
    nbins=30,
    title="Review Length Histogram"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# TOP ANIME
# --------------------------------------------------

st.subheader("🎌 Most Reviewed Anime")

top_anime = (
    df["anime_title"]
    .value_counts()
    .head(10)
    .reset_index()
)

top_anime.columns = [
    "Anime",
    "Reviews"
]

fig = px.bar(
    top_anime,
    x="Reviews",
    y="Anime",
    orientation="h",
    text="Reviews",
    title="Top Reviewed Anime"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# DATA SAMPLE
# --------------------------------------------------

st.subheader("🔍 Dataset Sample")

sample_cols = [
    "anime_title",
    "score",
    "binary_sentiment",
    "review_length"
]

st.dataframe(
    df[sample_cols].head(20),
    use_container_width=True
)
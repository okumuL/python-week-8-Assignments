import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Streamlit Page Setup ---
st.set_page_config(page_title="CORD-19 Data Explorer", page_icon="🧬", layout="wide")

st.title("🧬 CORD-19 Data Explorer")
st.markdown("""
Explore COVID-19 research trends interactively.
Use the filters below to explore publications across years, journals, and authors.
""")

# --- Load and Cache Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("./metadata_clean.csv", low_memory=False)
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    return df

df = load_data()

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filter Options")
min_year = int(df['publish_time'].dt.year.min())
max_year = int(df['publish_time'].dt.year.max())

year_range = st.sidebar.slider("Select Year Range", min_year, max_year, (2020, 2021))
keyword = st.sidebar.text_input("Search by Title Keyword")
journal_filter = st.sidebar.text_input("Filter by Journal Name (optional)")

# --- Filter Data ---
filtered_df = df.dropna(subset=['publish_time'])
filtered_df = filtered_df[
    (filtered_df['publish_time'].dt.year >= year_range[0]) &
    (filtered_df['publish_time'].dt.year <= year_range[1])
]

if keyword:
    filtered_df = filtered_df[filtered_df['title'].str.contains(keyword, case=False, na=False)]

if journal_filter:
    filtered_df = filtered_df[filtered_df['journal'].str.contains(journal_filter, case=False, na=False)]

# --- Display Summary ---
st.markdown(f"### 📄 {len(filtered_df):,} Papers Published Between {year_range[0]} and {year_range[1]}")
st.dataframe(filtered_df[['title', 'authors', 'journal', 'publish_time']].head(10), use_container_width=True)

# --- Visualizations Section ---
st.markdown("## 📊 Visual Insights")

col1, col2 = st.columns(2)

# 1️⃣ Papers per Year
with col1:
    st.subheader("Papers Published per Year")
    yearly_counts = filtered_df['publish_time'].dt.year.value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x=yearly_counts.index, y=yearly_counts.values, palette="coolwarm", ax=ax)
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Papers")
    ax.set_title("Publication Trend by Year")
    st.pyplot(fig)

# 2️⃣ Top Journals
with col2:
    st.subheader("Top Journals")
    top_journals = filtered_df['journal'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(y=top_journals.index, x=top_journals.values, palette="crest", ax=ax)
    ax.set_xlabel("Number of Papers")
    ax.set_ylabel("Journal")
    ax.set_title("Most Active Journals")
    st.pyplot(fig)

# 3️⃣ Authors with Most Publications
st.subheader("👩‍🔬 Top Authors by Number of Papers")
authors_series = filtered_df['authors'].dropna().str.split(';|,')
authors_flat = [author.strip() for sublist in authors_series for author in sublist if isinstance(sublist, list)]
authors_df = pd.Series(authors_flat).value_counts().head(10)

fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(y=authors_df.index, x=authors_df.values, palette="viridis", ax=ax)
ax.set_xlabel("Number of Papers")
ax.set_ylabel("Author")
ax.set_title("Top 10 Contributing Authors")
st.pyplot(fig)

# 4️⃣ Word Cloud of Titles (optional)
try:
    from wordcloud import WordCloud
    st.subheader("☁️ Common Words in Paper Titles")
    text = " ".join(filtered_df['title'].dropna())
    wc = WordCloud(width=800, height=400, background_color="white", colormap="cool").generate(text)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)
except ImportError:
    st.info("Install 'wordcloud' library to view title word cloud: `pip install wordcloud`")

# --- Footer ---
st.markdown("---")
st.caption("Built with ❤️ using Streamlit, pandas, and seaborn. © 2025 CORD-19 Data Explorer")



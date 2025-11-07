import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import numpy as np
from datetime import datetime

# Set page config
st.set_page_config(page_title="COVID-19 Research Papers Analysis", layout="wide")

# Title and description
st.title("COVID-19 Research Papers Analysis")
st.write("An interactive exploration of COVID-19 research papers dataset")

# Load and cache the data
@st.cache_data
def load_data():
    df = pd.read_csv('metadata.csv')
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    df['publication_year'] = df['publish_time'].dt.year
    if 'title' in df.columns:
        df['title_word_count'] = df['title'].str.split().str.len()
    if 'abstract' in df.columns:
        df['abstract_word_count'] = df['abstract'].str.split().str.len()
    return df

# Load the data
try:
    df = load_data()
    st.success("Data loaded successfully!")
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.stop()

# Sidebar filters
st.sidebar.header("Filters")

# Year range filter
min_year = int(df['publication_year'].min())
max_year = int(df['publication_year'].max())
year_range = st.sidebar.slider(
    "Select Year Range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# Filter data based on year range
filtered_df = df[
    (df['publication_year'] >= year_range[0]) & 
    (df['publication_year'] <= year_range[1])
]

# Main content
st.header("Dataset Overview")
st.write(f"Number of papers: {len(filtered_df)}")

# Publications over time
st.subheader("Publications Over Time")
yearly_counts = filtered_df['publication_year'].value_counts().sort_index()
fig, ax = plt.subplots(figsize=(10, 6))
yearly_counts.plot(kind='line', marker='o', ax=ax)
plt.title('Number of Publications Over Time')
plt.xlabel('Year')
plt.ylabel('Number of Publications')
plt.grid(True)
st.pyplot(fig)

# Top journals
if 'journal' in filtered_df.columns:
    st.subheader("Top Publishing Journals")
    n_journals = st.slider("Number of top journals to display", 5, 20, 10)
    top_journals = filtered_df['journal'].value_counts().head(n_journals)
    fig, ax = plt.subplots(figsize=(12, 6))
    top_journals.plot(kind='bar', ax=ax)
    plt.title(f'Top {n_journals} Journals Publishing COVID-19 Research')
    plt.xlabel('Journal')
    plt.ylabel('Number of Publications')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)

# Word cloud
if 'title' in filtered_df.columns:
    st.subheader("Title Word Cloud")
    text = ' '.join(filtered_df['title'].dropna())
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

# Sample of papers
st.subheader("Sample of Papers")
if st.checkbox("Show a sample of papers"):
    n_samples = st.slider("Number of papers to display", 5, 20, 5)
    columns_to_show = ['title', 'journal', 'publish_time']
    st.write(filtered_df[columns_to_show].sample(n=n_samples))

# Add footer
st.markdown("---")
st.markdown("Created with Streamlit • Data source: COVID-19 research papers dataset")
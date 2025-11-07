# COVID-19 Research Papers Analysis

This project analyzes a dataset of COVID-19 research papers using Python, Pandas, and Streamlit.

## Project Structure

- `covid19_research_analysis.ipynb`: Jupyter notebook containing detailed data analysis
- `app.py`: Streamlit application for interactive data exploration
- `metadata.csv`: Dataset containing COVID-19 research papers information

## Requirements

```
pandas
numpy
matplotlib
seaborn
streamlit
wordcloud
```

## Running the Application

1. Install the required packages:
```bash
pip install -r requirements.txt
```

2. Run the Streamlit app:
```bash
streamlit run app.py
```

The application will open in your default web browser.

## Features

- Interactive year range selection
- Publication trends over time
- Top publishing journals visualization
- Word cloud of paper titles
- Sample paper viewer

## Data Analysis

The Jupyter notebook (`covid19_research_analysis.ipynb`) contains:
- Basic data exploration
- Data cleaning and preparation
- Detailed analysis and visualizations
- Documentation of findings

## Notes

- The dataset is loaded from `metadata.csv`
- Missing values are handled appropriately
- Date formats are standardized
- New features are created for analysis

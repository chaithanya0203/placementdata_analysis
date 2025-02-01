import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="Student Performance Analytics",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
    <style>
    .main {
        background-color: #f0f8ff;
    }
    .stButton>button {
        background-color: #007bff;
        color: white;
        border-radius: 5px;
        padding: 10px 24px;
    }
    .st-emotion-cache-1v0mbdj {
        width: 100%;
    }
    h1, h2, h3 {
        color: #2c3e50;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('placementdata.csv')
    return df

def main():
    st.title("📊 Student Performance Analytics Dashboard")

    try:
        df = load_data()
    except Exception as e:
        st.error("Please ensure 'placementdata.csv' is in the correct location.")
        return

    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select Analysis",
                           ["Overview", "Academic Performance", "Skills Analysis", "Correlations"])

    if page == "Overview":
        show_overview(df)
    elif page == "Academic Performance":
        show_academic(df)
    elif page == "Skills Analysis":
        show_skills(df)
    else:
        show_correlations(df)

def show_overview(df):
    st.header("Dashboard Overview")

    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Students", len(df))
    with col2:
        avg_cgpa = df['CGPA'].mean().round(2)
        st.metric("Average CGPA", avg_cgpa)
    with col3:
        avg_aptitude = df['AptitudeTestScore'].mean().round(2)
        st.metric("Avg Aptitude Score", avg_aptitude)
    with col4:
        internship_rate = (df['Internships'].mean() * 100).round(2)
        st.metric("Avg Internships", internship_rate)

    # CGPA Distribution
    st.subheader("CGPA Distribution")
    fig = px.histogram(df, x='CGPA', nbins=20,
                      title='Distribution of CGPA Scores',
                      color_discrete_sequence=['#3498db'])
    fig.update_layout(bargap=0.1)
    st.plotly_chart(fig, use_container_width=True)

def show_academic(df):
    st.header("Academic Performance Analysis")

    # Academic Metrics Comparison
    fig = make_subplots(rows=1, cols=3,
                       subplot_titles=('CGPA Distribution', 'SSC Marks', 'HSC Marks'))

    fig.add_trace(go.Box(y=df['CGPA'], name='CGPA'), row=1, col=1)
    fig.add_trace(go.Box(y=df['SSC_Marks'], name='SSC'), row=1, col=2)
    fig.add_trace(go.Box(y=df['HSC_Marks'], name='HSC'), row=1, col=3)

    fig.update_layout(height=500, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    # Scatter plot: CGPA vs HSC
    fig = px.scatter(df, x='HSC_Marks', y='CGPA',
                    title='CGPA vs HSC Performance',
                    trendline="ols")
    st.plotly_chart(fig, use_container_width=True)

def show_skills(df):
    st.header("Skills and Activities Analysis")

    # Skills Overview
    col1, col2 = st.columns(2)

    with col1:
        fig = px.box(df, y='SoftSkillsRating',
                    title='Soft Skills Rating Distribution')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.histogram(df, x='ExtracurricularActivities',
                          title='Extracurricular Activities Distribution')
        st.plotly_chart(fig, use_container_width=True)

    # Projects vs Workshops comparison
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=df['Projects'], name='Projects'))
    fig.add_trace(go.Histogram(x=df['Workshops/Certifications'],
                              name='Workshops/Certifications'))
    fig.update_layout(barmode='overlay', title='Projects vs Workshops Distribution')
    st.plotly_chart(fig, use_container_width=True)

def show_correlations(df):
    st.header("Correlation Analysis")

    # Select only numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    corr_matrix = df[numeric_cols].corr()

    # Correlation heatmap
    fig = px.imshow(corr_matrix,
                    title='Correlation Matrix',
                    color_continuous_scale='RdBu')
    st.plotly_chart(fig, use_container_width=True)

    # Feature relationships
    st.subheader("Select Features to Compare")
    col1, col2 = st.columns(2)
    with col1:
        x_feature = st.selectbox('Select X-axis feature:', numeric_cols)
    with col2:
        y_feature = st.selectbox('Select Y-axis feature:', numeric_cols)

    fig = px.scatter(df, x=x_feature, y=y_feature,
                    title=f'{x_feature} vs {y_feature}',
                    trendline="ols")
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
